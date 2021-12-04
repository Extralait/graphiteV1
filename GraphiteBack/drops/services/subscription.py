from rest_framework import status
from rest_framework.response import Response

from drops.models import DropSubscription, Drop
from notifications.models import Notification


def add_subscription(user: int, drop: int):
    """
    Подписаться на дроп
    """
    drop_subscription, create = DropSubscription.objects.get_or_create(
        user_id=user,
        drop_id=drop
    )
    drop_owner = Drop.objects.get(pk=drop).owner.pk
    if create:
        Notification.objects.create(
            from_user_id=user,
            to_user_id=drop_owner,
            to_drop_id=drop,
            notification_type='drop_subscription'
        )
        return Response(status=status.HTTP_200_OK)
    else:
        if not drop_subscription.is_active:
            drop_subscription.is_active = True
            drop_subscription.save()
            return Response(status=status.HTTP_200_OK)
        return Response(
            {
                'detail': 'You already subscribe'
            },
            status=status.HTTP_400_BAD_REQUEST
        )


def delete_subscription(user: int, drop: int):
    """
    Удалить подписку на дроп
    """
    try:
        drop_subscription = DropSubscription.objects.ge(
            user_id=user,
            drop_id=drop
        )
        drop_subscription.is_active = False
        drop_subscription.save()
        return Response(status=status.HTTP_200_OK)
    except Drop.DoesNotExist:
        return Response(
            {
                'detail': 'You are not subscribe'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
