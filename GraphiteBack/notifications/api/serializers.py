from rest_framework import serializers

from notifications.models import Notification
from users.api.serializers import UserListSerializer


class NotificationSerializer(serializers.ModelSerializer):
    """
    Уведомления (Сериализатор)
    """
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(NotificationSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['notification_type','from_user','to_user',
                            'to_drop','to_collection','header','body',
                            'is_active','details']

