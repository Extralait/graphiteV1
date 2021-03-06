from pprint import pprint

from django.db.models import Q
from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
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
from drops.services.like import delete_like, add_like
from drops.services.subscription import delete_subscription, add_subscription
from drops.services.view import add_view
from drops_collections.models import SpecialCollection
from offers.services.offer_operations import make_offer, delete_offer
from transactions.services.transaction_operations import buy_drop
from utils.pagination import StandardResultsSetPagination
from utils.parsers import MultipartJsonParser
from utils.permissions import OwnerOrAdmin


class DropViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    Дроп (Представление)
    """
    parser_classes = [JSONParser, MultipartJsonParser]

    pagination_class = StandardResultsSetPagination
    filter_fields = [f.name for f in Drop._meta.fields + Drop._meta.related_objects
                     if not (f.__dict__.get('upload_to') or f.name == 'name')]
    ordering_fields = filter_fields
    ordering_fields.append('name')

    def get_serializer_context(self):
        context = super(DropViewSet, self).get_serializer_context()

        if len(self.request.FILES) > 0:
            context.update({
                'included_images': self.request.FILES
            })
        return context

    def get_permissions(self):
        """
        Возвращает права доступа
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = (AllowAny,)
        elif self.action in ['create', 'buy_drop', 'on_auction']:
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
        elif self.action in ['list', 'on_auction']:
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

    def get_queryset(self):
        self.request.query_params._mutable = True
        name_query = self.request.query_params.get('name', None)
        self.request.query_params.pop('name', None)
        if name_query:
            queryset = self.filter_queryset(Drop.objects.filter(
                Q(name__icontains=name_query)
                | Q(from_collection__name__icontains=name_query)
                | Q(artist__first_name__icontains=name_query)
                | Q(artist__last_name__icontains=name_query)
            ).all())
        else:
            queryset = self.filter_queryset(Drop.objects.all())
        return self.filter_queryset_by_parents_lookups(
            queryset
        )

    def _is_owner(self):
        detail_drop_pk = self.kwargs.get('pk')
        if not detail_drop_pk:
            return False
        current_user_pk = self.request.user.pk
        drop_owner_pk = Drop.objects.get(pk=detail_drop_pk).owner.pk
        return drop_owner_pk == current_user_pk

    def create(self, request, **kwargs):
        self.request.data.pop('picture_small', None)
        self.request.data.pop('picture_big', None)
        serializer = self.get_serializer(data=self.request.data)
        result = serializer.create(self.request.data)

        if serializer.is_valid():
            return Response(self.get_serializer(result).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)

    def update(self, request, **kwargs):
        self.request.data.pop('picture_small', None)
        self.request.data.pop('picture_big', None)
        serializer = self.get_serializer(data=self.request.data)
        instance = Drop.objects.get(pk=self.kwargs.get('pk'))
        result = serializer.update(instance=instance, validated_data=self.request.data)

        if serializer.is_valid():
            return Response(self.get_serializer(result).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)

    @action(
        detail=False,
        methods=['get'],
        name='on-auction',
        url_path='on-auction',
        permission_classes=(IsAuthenticated,),
    )
    def on_auction(self, request, **kwargs):
        """
        Получить мой профиль
        """

        queryset = Drop.objects.filter(
            auction__auction_user_bid__user=self.request.user,
            auction__auction_user_bid__is_active=True,
        ).distinct('pk')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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

    @make_offer.mapping.delete
    def delete_offer(self, request, **kwargs):
        """
        Удаление предложения
        """
        if self._is_owner():
            return Response(
                {
                    'detail': 'It is impossible to delete offer on yourself drop'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return delete_offer(drop=int(self.kwargs.get('pk')),
                                buyer=int(self.request.user.pk))


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
