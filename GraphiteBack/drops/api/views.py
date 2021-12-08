from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from drops.api.serializers import (
    DropListSerializer,
    DropDetailsSerializer,
    DropCreateOrUpdateSerializer, DropBuySerializer, MakeOfferSerializer, SpecialCollectionSerializer, TagSerializer,
    CategorySerializer
)
from drops.models import Drop, Tag, Category
from drops_collections.models import SpecialCollection
from offers.services.offer_operations import make_offer
from transactions.services.transaction_operations import buy_drop
from drops.services.like import delete_like, add_like
from drops.services.subscription import delete_subscription, add_subscription
from drops.services.view import add_view
from utils.pagination import StandardResultsSetPagination
from utils.permissions import OwnerOrAdmin


class DropViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    Дроп (Представление)
    """
    pagination_class = StandardResultsSetPagination
    queryset = Drop.objects.all()
    filter_fields = [f.name for f in Drop._meta.fields + Drop._meta.related_objects if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields

    def get_permissions(self):
        """
        Возвращает права доступа
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = (AllowAny,)
        elif self.action in ['create', 'buy_drop']:
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
            serializer_class = DropListSerializer
        elif self.action == 'buy_drop':
            serializer_class = DropBuySerializer
        elif self.action == 'make_offer':
            serializer_class = MakeOfferSerializer
        elif self.action in ['update', 'partial_update', 'create']:
            serializer_class = DropCreateOrUpdateSerializer
        else:
            serializer_class = DropDetailsSerializer

        return serializer_class

    def _is_owner(self):
        detail_drop_pk = self.kwargs.get('pk')
        if not detail_drop_pk:
            return False
        current_user_pk = self.request.user.pk
        drop_owner_pk = Drop.objects.get(pk=detail_drop_pk).owner.pk
        return drop_owner_pk == current_user_pk

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
                    'detail': 'It is impossible to add subscription to yourself drop'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return add_subscription(drop=int(self.kwargs.get('pk')),
                                    user=int(self.request.user.pk))

    @add_subscription.mapping.delete
    def delete_subscription(self, request, **kwargs):
        """
        Удаление подписки на коллекцию
        """
        if self._is_owner():
            return Response(
                {
                    'detail': 'It is impossible to delete subscription to yourself drop'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return delete_subscription(drop=int(self.kwargs.get('pk')),
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
                    'detail': 'It is impossible to add like to yourself drop'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return add_like(drop=int(self.kwargs.get('pk')),
                            user=int(self.request.user.pk))

    @add_like.mapping.delete
    def delete_like(self, request, **kwargs):
        """
        Удаление лайка на коллекции
        """
        if self._is_owner():
            return Response(
                {
                    'detail': 'It is impossible to delete like to yourself drop'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return delete_like(drop=int(self.kwargs.get('pk')),
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
                    'detail': 'It is impossible to add viewing to yourself drop'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return add_view(drop=int(self.kwargs.get('pk')),
                            user=int(self.request.user.pk))

    @action(
        detail=True,
        methods=['post'],
        name='buy-drop',
        url_path='buy-drop',
        permission_classes=(IsAuthenticated,),
    )
    def buy_drop(self, request, **kwargs):
        """
        Покупка дропа
        """

        if self._is_owner():
            return Response(
                {
                    'detail': 'It is impossible to buy yourself drop'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                count = serializer.validated_data['count']

                return buy_drop(drop_pk=int(self.kwargs.get('pk')),
                                count=count,
                                buyer=self.request.user)
            else:
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

    @action(
        detail=True,
        methods=['post'],
        name='make-offer',
        url_path='make-offer',
        permission_classes=(IsAuthenticated,),
    )
    def make_offer(self, request, **kwargs):
        """
        Сделать офер
        """
        if self._is_owner():
            return Response(
                {
                    'detail': 'It is impossible to make offer on yourself drop'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                count = serializer.validated_data['count']
                unit_price = serializer.validated_data['unit_price']

                return make_offer(drop_pk=int(self.kwargs.get('pk')),
                                  count=count,
                                  unit_price=unit_price,
                                  buyer=self.request.user)
            else:
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )


class SpecialCollectionViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    Специальная коллекция (Представление)
    """
    queryset = SpecialCollection.objects.all()
    serializer_class = SpecialCollectionSerializer

    def get_permissions(self):
        """
        Возвращает права доступа
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAdminUser,)

        return [permission() for permission in permission_classes]


class TagViewSet(viewsets.ModelViewSet):
    """
    Тег дропа (Представление)
    """
    pagination_class = StandardResultsSetPagination
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        """
        Возвращает права доступа
        """
        if self.action in ['create', 'list', 'retrieve']:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAdminUser,)

        return [permission() for permission in permission_classes]


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Категория дропа (Представление)
    """
    pagination_class = StandardResultsSetPagination
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        """
        Возвращает права доступа
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAdminUser,)

        return [permission() for permission in permission_classes]

