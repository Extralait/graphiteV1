from rest_framework import status
from rest_framework.response import Response
from bulk_update.helper import bulk_update

from auction.models import Auction, AuctionUserBid
from config.celery import app as celery_app
from transactions.services.transaction_operations import buy_drop


@celery_app.task(name='api.task.auction_waiter', queue='multi_task', routing_key='multi_task')
def auction_waiter(auction_id):
    end_auction.delay(auction_id)


@celery_app.task(name='api.task.end_auction', queue='solo_task', routing_key='solo_task')
def end_auction(auction_id):
    auction = Auction.objects.get(pk=auction_id)
    drop = auction.drop
    if auction.current_user:
        buy_drop(
            drop_pk=auction.drop.pk,
            count=auction.sell_count,
            buyer= auction.current_user,
            unit_price=auction.current_cost
        )
    drop.to_sell = False
    drop.save()

    bids,users = [],[]
    for auction_bid in auction.auction_user_bid.filter(is_active=True).select_related('user').all():
        user = auction_bid.user
        if user != auction.current_user:
            user.balance += auction_bid.bid*auction.sell_count
            users.append(user)
        auction_bid.is_active=False
        bids.append(auction_bid)

    bulk_update(bids)
    bulk_update(users)

    auction.is_active = False
    auction.save()


def place_bid(auction_id, user, bid):
    auction = Auction.objects.get(pk=auction_id)
    if not auction.is_active:
        return Response(
            {
                'detail': 'Auction not active'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if auction.current_cost == auction.init_cost:
        if bid < auction.init_cost:
            return Response(
                {
                    'detail': 'Too low bid'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
    elif auction.min_rate > bid - auction.current_cost:
        return Response(
            {
                'detail': 'Too low bid'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    previous_bid = None
    try:
        previous_bid = AuctionUserBid.objects.get(
            user=user,
            auction=auction,
            is_active=True
        )
        bid_difference = previous_bid.bid

    except AuctionUserBid.DoesNotExist:
        bid_difference = bid

    if user.balance < bid_difference*auction.sell_count:
        return Response(
            {
                'detail': 'Too low balance'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if previous_bid:
        previous_bid.is_active = False
        previous_bid.save()

    user.balance -= bid_difference*auction.sell_count
    user.save()
    auction.current_cost = bid
    auction.current_user = user
    auction.save()

    AuctionUserBid.objects.create(
        user=user,
        auction=auction,
        bid=bid
    )
    return Response(
        status=status.HTTP_200_OK
    )


def delete_bid(auction_id, user):
    try:
        auction_bid = AuctionUserBid.objects.get(
            auction_id=auction_id,
            user=user,
            is_active=True
        )
    except AuctionUserBid.DoesNotExist:
        return Response(
            {
                'detail': 'You don`t have bid on this auction'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    auction = Auction.objects.get(pk=auction_id)
    if not auction.is_active:
        return Response(
            {
                'detail': 'Auction not active'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    if auction.current_user == user:
        if auction.auction_user_bid.filter(is_active=True).count() == 1:
            auction.current_user = None
            auction.current_cost = auction.init_cost
        else:
            next_bid = auction.auction_user_bid.filter(is_active=True).order_by('-bid')[0]
            auction.current_user = next_bid.user
            auction.current_cost = next_bid.bid
        auction.save()

    user.balance += auction_bid.bid*auction.sell_count
    user.save()
    auction_bid.is_active = False
    auction_bid.save()
    return Response(
        status=status.HTTP_200_OK
    )

# @shared_task(name='main.tasks.update_all_portfolios', queue='ml_task', routing_key='ml_task')
# def example_shared_task():
#     pass
