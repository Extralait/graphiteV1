from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from drops_collections.api.serializers import (
    CollectionListSerializer,
    CollectionDetailsSerializer,
    CurrentUserCollectionDetailsSerializer
)
from drops.api.serializers import SpecialCollectionSerializer
from drops_collections.models import Collection, SpecialCollection
from drops_collections.services.like import add_like, delete_like
from drops_collections.services.subscription import add_subscription, delete_subscription
from drops_collections.services.view import add_view
from utils.pagination import StandardResultsSetPagination
from utils.permissions import OwnerOrAdmin, Nobody


class CollectionViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = Collection.objects.all()
    filter_fields = [f.name for f in Collection._meta.fields + Collection._meta.related_objects if
                     not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields

    def _is_owner(self):
        detail_collection_pk = self.kwargs.get('pk')
        if not detail_collection_pk:
            return False
        current_user_pk = self.request.user.pk
        collection_owner_pk = Collection.objects.get(pk=detail_collection_pk).owner.pk
        return collection_owner_pk == current_user_pk

    def get_permissions(self):
        """
        Возвращает права доступа
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = (AllowAny,)
        elif self.action == 'create':
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (OwnerOrAdmin,)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Возвращает класс сериализатора
        """
        if self.action in ['add_subscription', 'add_view', 'add_like']:
            serializer_class = serializers.Serializer
        elif self.action == 'list':
            serializer_class = CollectionListSerializer
        else:
            if self._is_owner():
                serializer_class = CurrentUserCollectionDetailsSerializer
            else:
                serializer_class = CollectionDetailsSerializer

        return serializer_class

    @action(
        detail=True,
        methods=['post'],
        name='subscription',
        url_path='subscription',
        permission_classes=(IsAuthenticated,),
    )
    def add_subscription(self, request, **kwargs):
        """
        Создание подписки на коллекцию
        """
        if self._is_owner():
            return Response(
                {
                    'detail': 'It is impossible to add subscription to yourself collection'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return add_subscription(collection=int(self.kwargs.get('pk')),
                                    user=int(self.request.user.pk))

    @add_subscription.mapping.delete
    def delete_subscription(self, request, **kwargs):
        """
        Удаление подписки на коллекцию
        """
        if self._is_owner():
            return Response(
                {
                    'detail': 'It is impossible to delete subscription to yourself collection'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return delete_subscription(collection=int(self.kwargs.get('pk')),
                                       user=int(self.request.user.pk))

    @action(
        detail=True,
        methods=['post'],
        name='like',
        url_path='like',
        permission_classes=(IsAuthenticated,),
    )
    def add_like(self, request, **kwargs):
        """
        Создание лайка на коллекции
        """
        if self._is_owner():
            return Response(
                {
                    'detail': 'It is impossible to add like to yourself collection'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return add_like(collection=int(self.kwargs.get('pk')),
                            user=int(self.request.user.pk))

    @add_like.mapping.delete
    def delete_like(self, request, **kwargs):
        """
        Удаление лайка на коллекции
        """
        if self._is_owner():
            return Response(
                {
                    'detail': 'It is impossible to delete like to yourself collection'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return delete_like(collection=int(self.kwargs.get('pk')),
                               user=int(self.request.user.pk))

    @action(
        detail=True,
        methods=['post'],
        name='viewing',
        url_path='viewing',
        permission_classes=(IsAuthenticated,),
    )
    def add_view(self, request, **kwargs):
        """
        Создание просмотра коллекции
        """
        if self._is_owner():
            return Response(
                {
                    'detail': 'It is impossible to add viewing to yourself collection'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return add_view(collection=int(self.kwargs.get('pk')),
                            user=int(self.request.user.pk))


class SpecialCollectionViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = SpecialCollection.objects.all()
    filter_fields = [f.name for f in SpecialCollection._meta.fields + SpecialCollection._meta.related_objects if
                     not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields
    serializer_class = SpecialCollectionSerializer

    def get_permissions(self):
        """
        Возвращает права доступа
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (Nobody,)

        return [permission() for permission in permission_classes]
