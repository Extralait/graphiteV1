from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from rest_framework import status, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from offers.api.serializers import OfferSerializer
from offers.models import Offer
from offers.services.offer_operations import confirm
from utils.pagination import StandardResultsSetPagination
from utils.permissions import OwnerOrAdmin, ParticipantsOrAdmin, Nobody


class OfferViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_fields = [f.name for f in Offer._meta.fields + Offer._meta.related_objects if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields

    def _is_owner(self):
        detail_offer_pk = self.kwargs.get('pk')
        if not detail_offer_pk:
            return False
        current_user_pk = self.request.user.pk
        offer_owner_pk = Offer.objects.get(pk=detail_offer_pk).owner.pk
        return offer_owner_pk == current_user_pk

    def get_permissions(self):
        """
        Возвращает права доступа
        """
        if self.action in ['list', 'retrieve', 'destroy']:
            permission_classes = (ParticipantsOrAdmin,)
        elif self.action in ['confirm', None]:
            permission_classes = (OwnerOrAdmin,)
        else:
            permission_classes = (Nobody,)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Возвращает класс сериализатора
        """
        if self.action in ['confirm']:
            serializer_class = serializers.Serializer
        else:
            serializer_class = OfferSerializer
        return serializer_class

    def filter_queryset(self, queryset):

        user = self.request.user
        if user.is_staff:
            pass
        elif type(self.request.user) == AnonymousUser:
            return queryset.none()
        else:
            queryset = queryset.filter(Q(buyer=user) | Q(owner=user))
        return queryset

    @action(
        detail=True,
        methods=['post'],
        name='confirm',
        permission_classes=(OwnerOrAdmin,),
    )
    def confirm(self, request, **kwargs):
        """
        Подтверждение предложения
        """
        if not self._is_owner():
            return Response(
                {
                    'detail': 'It is impossible to confirm offer for other user'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return confirm(Offer.objects.get(pk=self.kwargs.get('pk')))
