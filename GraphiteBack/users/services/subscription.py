from rest_framework import status
from rest_framework.response import Response

from notifications.models import Notification
from users.models import UserSubscription


def add_subscription(subscriber: int, subscription: int):
    """
    Подписаться на пользователя
    """
    user_subscription, create = UserSubscription.objects.get_or_create(
        subscriber_id=subscriber,
        subscription_id=subscription
    )
    if create:
        Notification.objects.create(
            from_user_id=subscriber,
            to_user_id=subscription,
            notification_type='user_subscription'
        )
        return Response(status=status.HTTP_200_OK)
    else:
        if not user_subscription.is_active:
            user_subscription.is_active = True
            user_subscription.save()
            return Response(status=status.HTTP_200_OK)
        return Response(
            {
                'detail': 'You already subscribe'
            },
            status=status.HTTP_400_BAD_REQUEST
        )


def delete_subscription(subscriber: int, subscription: int):
    """
    Удалить подписку на пользователя
    """
    try:
        user_subscription = UserSubscription.objects.get(
            subscriber_id=subscriber,
            subscription_id=subscription
        )
        user_subscription.is_active = False
        user_subscription.save()
        return Response(status=status.HTTP_200_OK)
    except UserSubscription.DoesNotExist:
        return Response(
            {
                'detail': 'You are not subscribe'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
