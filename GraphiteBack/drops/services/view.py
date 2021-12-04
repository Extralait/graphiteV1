from rest_framework import status
from rest_framework.response import Response

from drops.models import Drop, DropView
from notifications.models import Notification


def add_view(user: int, drop: int):
    """
    Добавить просмотр дропа
    """
    user_view, create = DropView.objects.get_or_create(
        user_id=user,
        drop_id=drop
    )
    drop_owner = Drop.objects.get(pk=drop).owner.pk
    if create:
        Notification.objects.create(
            from_user_id=user,
            to_user_id=drop_owner,
            to_drop_id=drop,
            notification_type='drop_view'
        )
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(
            {
                'detail': 'You already viewed'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
