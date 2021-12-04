from rest_framework import status
from rest_framework.response import Response

from notifications.models import Notification
from users.models import UserView


def add_view(looking: int, overlooked: int):
    """
    Добавить просмотр пользователя
    """
    user_view, create = UserView.objects.get_or_create(
        looking_id=looking,
        overlooked_id=overlooked
    )
    if create:
        Notification.objects.create(
            from_user_id=looking,
            to_user_id=overlooked,
            notification_type='user_subscription'
        )
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(
            {
                'detail': 'You already viewed'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
