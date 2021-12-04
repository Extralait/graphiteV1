from rest_framework import status
from rest_framework.response import Response

from drops.models import DropLike, Drop
from notifications.models import Notification


def add_like(user: int, drop: int):
    """
    Поставить лайк на коллекции
    """
    drop_like, create = DropLike.objects.get_or_create(
        user_id=user,
        drop_id=drop
    )
    drop_owner = Drop.objects.get(pk=drop).owner.pk
    if create:
        Notification.objects.create(
            from_user_id=user,
            to_user_id=drop_owner,
            to_drop_id=drop,
            notification_type='drop_like'
        )
        return Response(status=status.HTTP_200_OK)
    else:
        if not drop_like.is_active:
            drop_like.is_active = True
            drop_like.save()
            return Response(status=status.HTTP_200_OK)
        return Response(
            {
                'detail': 'You already like'
            },
            status=status.HTTP_400_BAD_REQUEST
        )


def delete_like(user: int, drop: int):
    """
    Удалить лайк на коллекции
    """
    try:
        drop_like = DropLike.objects.ge(
            user_id=user,
            drop_id=drop
        )
        drop_like.is_active = False
        drop_like.save()
        return Response(status=status.HTTP_200_OK)
    except Drop.DoesNotExist:
        return Response(
            {
                'detail': 'You did not like'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
