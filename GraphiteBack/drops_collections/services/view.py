from rest_framework import status
from rest_framework.response import Response

from drops_collections.models import Collection, CollectionView
from notifications.models import Notification


def add_view(user: int, collection: int):
    """
    Добавить просмотр коллекции
    """
    user_view, create = CollectionView.objects.get_or_create(
        user_id=user,
        collection_id=collection
    )
    collection_owner = Collection.objects.get(pk=collection).owner.pk
    if create:
        Notification.objects.create(
            from_user_id=user,
            to_user_id=collection_owner,
            to_collection_id = collection,
            notification_type='collection_view'
        )
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(
            {
                'detail': 'You already viewed'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
