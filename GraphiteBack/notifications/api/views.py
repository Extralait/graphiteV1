from rest_framework import viewsets
from rest_framework_extensions.mixins import NestedViewSetMixin

from notifications.api.serializers import NotificationSerializer
from notifications.models import Notification
from utils.pagination import StandardResultsSetPagination
from utils.permissions import Nobody, AddresseeOrAdmin


class NotificationViewSet(NestedViewSetMixin,viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filter_fields = [f.name for f in Notification._meta.fields + Notification._meta.related_objects if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields

    def get_permissions(self):
        """
        Возвращает права доступа
        """
        if self.action == 'create':
            permission_classes = (Nobody,)
        else:
            permission_classes = (AddresseeOrAdmin,)

        return [permission() for permission in permission_classes]

    def filter_queryset(self, queryset):
        user = self.request.user
        if user.is_staff:
            pass
        else:
            queryset = queryset.filter(to_user=user)
        return queryset
