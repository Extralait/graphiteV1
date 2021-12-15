from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets
from rest_framework_extensions.mixins import NestedViewSetMixin

from notifications.api.serializers import NotificationSerializer
from notifications.models import Notification
from utils.pagination import StandardResultsSetPagination
from utils.permissions import Nobody, AddresseeOrAdmin


class NotificationViewSet(NestedViewSetMixin,viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
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

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Notification.objects.all()
        elif type(self.request.user) == AnonymousUser:
            queryset = Notification.objects.none()
        else:
            queryset = Notification.objects.filter(to_user=user).all()
        return self.filter_queryset_by_parents_lookups(
            queryset
        )
