from rest_framework import status
from rest_framework.response import Response

from drops_collections.models import CollectionSubscription, Collection, CollectionLike
from notifications.models import Notification


def add_like(user: int, collection: int):
    """
    Поставить лайк на коллекции
    """
    collection_like, create = CollectionLike.objects.get_or_create(
        user_id=user,
        collection_id=collection
    )
    collection_owner = Collection.objects.get(pk=collection).owner.pk
    if create:
        Notification.objects.create(
            from_user_id=user,
            to_user_id=collection_owner,
            to_collection_id=collection,
            notification_type='collection_like'
        )
        return Response(status=status.HTTP_200_OK)
    else:
        if not collection_like.is_active:
            collection_like.is_active = True
            collection_like.save()
            return Response(status=status.HTTP_200_OK)
        return Response(
            {
                'detail': 'You already like'
            },
            status=status.HTTP_400_BAD_REQUEST
        )


def delete_like(user: int, collection: int):
    """
    Удалить лайк на коллекции
    """
    try:
        collection_like = CollectionLike.objects.ge(
            user_id=user,
            collection_id=collection
        )
        collection_like.is_active = False
        collection_like.save()
        return Response(status=status.HTTP_200_OK)
    except Collection.DoesNotExist:
        return Response(
            {
                'detail': 'You did not like'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
