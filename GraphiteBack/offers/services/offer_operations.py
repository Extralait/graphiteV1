from rest_framework import status
from rest_framework.response import Response

from drops.models import Drop
from notifications.models import Notification
from offers.api.serializers import OfferSerializer
from offers.models import Offer
from transactions.services.transaction_operations import buy_drop
from users.models import User


def make_offer(drop_pk: int, count: int, unit_price: float, buyer: User):
    owner_drop = Drop.objects.get(pk=drop_pk)

    in_stock = owner_drop.in_stock
    drop_name = owner_drop.name
    owner_pk = owner_drop.owner.pk

    if in_stock < count:
        return Response(
            {
                'detail': 'Not enough copies available'
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    offer = Offer.objects.create(
        drop_id=drop_pk,
        buyer_id=buyer.pk,
        copies_count=count,
        unit_price=unit_price
    )

    Notification.objects.create(
        from_user_id=buyer.pk,
        to_user_id=owner_pk,
        to_drop_id=drop_pk,
        notification_type='offer',
        body=f'{buyer} offered to buy {count} copies of your drop {drop_name} with unit price {unit_price}'
    )

    return Response(
        OfferSerializer(offer).data,
        status=status.HTTP_200_OK
    )


def confirm(offer: Offer):
    offer.is_active = False
    offer.save()
    drop_pk = offer.drop.pk
    count = offer.copies_count
    buyer = offer.buyer
    unit_price = offer.unit_price

    response = buy_drop(drop_pk, count, buyer, unit_price)

    Notification.objects.create(
        from_user_id=offer.owner.pk,
        to_user_id=buyer.pk,
        to_drop_id=drop_pk,
        notification_type='confirm_offer',
        body=f'{offer.owner} confirm your offer to buy {count} copies of '
             f'him drop {offer.drop} with unit price {unit_price}'
    )

    return response
