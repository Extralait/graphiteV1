from rest_framework import status
from rest_framework.response import Response

from drops_collections.models import CollectionSubscription, Collection
from notifications.models import Notification


def add_subscription(user: int, collection: int):
    """
    Подписаться на коллекцию
    """
    collection_subscription, create = CollectionSubscription.objects.get_or_create(
        user_id=user,
        collection_id=collection
    )
    collection_owner = Collection.objects.get(pk=collection).owner.pk
    if create:
        Notification.objects.create(
            from_user_id=user,
            to_user_id=collection_owner,
            to_collection_id=collection,
            notification_type='collection_subscription'
        )
        return Response(status=status.HTTP_200_OK)
    else:
        if not collection_subscription.is_active:
            collection_subscription.is_active = True
            collection_subscription.save()
            return Response(status=status.HTTP_200_OK)
        return Response(
            {
                'detail': 'You already subscribe'
            },
            status=status.HTTP_400_BAD_REQUEST
        )


def delete_subscription(user: int, collection: int):
    """
    Удалить подписку на коллекцию
    """
    try:
        collection_subscription = CollectionSubscription.objects.ge(
            user_id=user,
            collection_id=collection
        )
        collection_subscription.is_active = False
        collection_subscription.save()
        return Response(status=status.HTTP_200_OK)
    except Collection.DoesNotExist:
        return Response(
            {
                'detail': 'You are not subscribe'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
