from rest_framework import status
from rest_framework.response import Response

from drops.models import Drop
from notifications.models import Notification
from transactions.api.serializers import TransactionSerializer
from transactions.models import Transaction
from users.models import User


def buy_drop(drop_pk: int, count: int, buyer: User, unit_price=None):
    """
    Купить дроп
    """
    buyer_pk = buyer.pk
    try:
        buyer_drop = Drop.objects.get(owner_id=buyer_pk, parent_id=drop_pk)
    except Drop.DoesNotExist:
        buyer_drop = None

    owner_drop = Drop.objects.get(pk=drop_pk)

    if owner_drop.sell_type != 'sell' or not owner_drop.to_sell:
        return Response(
            {
                'detail': 'This drop not for sale'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    sell_count = owner_drop.sell_count

    if sell_count < count:
        return Response(
            {
                'detail': 'Not enough copies available'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    owner_drop.sell_count -= count
    owner_drop.in_stock -= count
    owner_drop.save()
    owner_drop_name = owner_drop.name
    owner_pk = owner_drop.owner.pk
    if buyer_drop:
        owner_drop.in_stock += count
        owner_drop.save()
    else:
        owner_drop.pk = None
        buyer_drop = owner_drop
        buyer_drop.sell_count = 0
        buyer_drop.in_stock = count
        buyer_drop.parent_id = drop_pk
        buyer_drop.owner_id = buyer_pk
        buyer_drop.to_sell = False
        buyer_drop.from_collection = None
        buyer_drop.save()

    transaction = Transaction.objects.create(
        drop_id=drop_pk,
        buyer=buyer,
        copies_count=count,
        unit_price=unit_price
    )

    Notification.objects.create(
        from_user_id=buyer_pk,
        to_user_id=owner_pk,
        to_drop_id=drop_pk,
        notification_type='drop_buy',
        body=f'{buyer} buy {count} copies of your drop {owner_drop_name}'
    )

    return Response(
        TransactionSerializer(transaction).data,
        status=status.HTTP_200_OK
    )