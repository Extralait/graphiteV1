from django.db.models import Q
from rest_framework import viewsets
from rest_framework_extensions.mixins import NestedViewSetMixin

from transactions.api.serializers import TransactionSerializer
from transactions.models import Transaction
from utils.pagination import StandardResultsSetPagination
from utils.permissions import Nobody, ParticipantsOrAdmin, OwnerOrAdmin


class TransactionViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_fields = [f.name for f in Transaction._meta.fields + Transaction._meta.related_objects if
                     not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields

    def get_permissions(self):
        """
        Возвращает права доступа
        """
        if self.action in ['list', 'retrieve', 'destroy']:
            permission_classes = (ParticipantsOrAdmin,)
        else:
            permission_classes = (Nobody,)

        return [permission() for permission in permission_classes]

    def filter_queryset(self, queryset):
        user = self.request.user
        if user.is_staff:
            pass
        else:
            queryset = queryset.filter(Q(buyer=user) | Q(owner=user))
        return queryset
