from django.db.models import Count, Sum, F, FloatField
from djoser.permissions import CurrentUserOrAdmin
from djoser.serializers import UserCreateSerializer
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from users.api.serializers import (
    UserDetailsSerializer,
    CurrentUserDetailsSerializer,
    UserListSerializer,
    PassportDataSerializer, UsersGroupSerializer
)
from users.models import User, PassportData, UsersGroup
from users.services.subscription import add_subscription, delete_subscription
from users.services.view import add_view
from utils.pagination import StandardResultsSetPagination
from utils.permissions import Nobody


class UserProfileViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = User.objects.all()
    filter_fields = [f.name for f in User._meta.fields + User._meta.related_objects if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields

    def _is_current_user(self):
        detail_user_pk = self.kwargs.get('pk')
        if not detail_user_pk:
            return False
        current_user_pk = self.request.user.pk
        return int(detail_user_pk) == current_user_pk

    def update_me(self, data):
        user = self.request.user
        serializer = self.get_serializer(
            instance=user,
            data=data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def update_my_passport(self, data):
        user = self.request.user
        passport_data = PassportData.objects.get(user_id=user.pk)
        serializer = self.get_serializer(
            instance=passport_data,
            data=data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        """
        Возвращает права доступа
        """
        if self.action in ['list', 'retrieve', 'create','expensive_artists']:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (CurrentUserOrAdmin,)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Возвращает класс сериализатора
        """
        if self.action == 'create':
            serializer_class = UserCreateSerializer
        elif self.action in ['add_subscription', 'add_view']:
            serializer_class = serializers.Serializer
        elif self.action in ['me', 'patch_me', 'put_me', 'delete_me']:
            serializer_class = CurrentUserDetailsSerializer
        elif self.action in ['my_passport', 'patch_my_passport', 'put_my_passport', ]:
            serializer_class = PassportDataSerializer
        elif self.action == 'list':
            serializer_class = UserListSerializer
        elif self.action == 'expensive_artists':
            serializer_class = UserDetailsSerializer
        else:
            if self._is_current_user():
                serializer_class = CurrentUserDetailsSerializer
            else:
                serializer_class = UserDetailsSerializer

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
        Создание подписки на пользователя
        """
        if self._is_current_user():
            return Response(
                {
                    'detail': 'It is impossible to add subscription to yourself'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return add_subscription(subscription=int(self.kwargs.get('pk')),
                                    subscriber=int(self.request.user.pk))

    @add_subscription.mapping.delete
    def delete_subscription(self, request, **kwargs):
        """
        Удаление подписки на пользователя
        """
        if self._is_current_user():
            return Response(
                {
                    'detail': 'It is impossible to delete subscription to yourself'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return delete_subscription(subscription=int(self.kwargs.get('pk')),
                                       subscriber=int(self.request.user.pk))

    @action(
        detail=True,
        methods=['post'],
        name='viewing',
        url_path='viewing',
        permission_classes=(IsAuthenticated,),
    )
    def add_view(self, request, **kwargs):
        """
        Создание просмотра профиля пользователя
        """
        if self._is_current_user():
            return Response(
                {
                    'detail': 'It is impossible to add viewing to yourself'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return add_view(overlooked=int(self.kwargs.get('pk')),
                            looking=int(self.request.user.pk))

    @action(
        detail=False,
        methods=['get'],
        name='me',
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request, **kwargs):
        """
        Получить мой профиль
        """
        queryset = self.request.user
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    @me.mapping.patch
    def patch_me(self, request, **kwargs):
        return self.update_me(request.data)

    @me.mapping.put
    def put_me(self, request, **kwargs):
        return self.update_me(request.data)

    @me.mapping.delete
    def delete_me(self, request, **kwargs):
        user = self.request.user
        user.delete()
        return Response(status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get'],
        name='my-passport',
        url_path='my-passport',
        permission_classes=(IsAuthenticated,),
    )
    def my_passport(self, request, **kwargs):
        """
        Получить мой паспорт
        """
        queryset = PassportData.objects.get(user=self.request.user)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    @my_passport.mapping.patch
    def patch_my_passport(self, request, **kwargs):
        """
        Частично обновить мой паспорт
        """
        return self.update_my_passport(request.data)

    @my_passport.mapping.put
    def put_my_passport(self, request, **kwargs):
        """
        Обновить мой паспорт
        """
        return self.update_my_passport(request.data)

    @action(
        detail=False,
        methods=['get'],
        name='expensive-artists',
        url_path='expensive-artists',
        permission_classes=(AllowAny,),
    )
    def expensive_artists(self, request, **kwargs):
        """
        Получить дорогих художников
        """
        expensive_artists = (
                                User.objects
                                    .annotate(proceeds=Sum(
                                        F('owner_transactions__unit_price') * F('owner_transactions__copies_count'),
                                        output_field=FloatField()))
                                    .order_by('proceeds'))[:20]

        page = self.paginate_queryset(expensive_artists)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(expensive_artists, many=True)
        return Response(serializer.data)


class UsersGroupViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = UsersGroup.objects.all()
    filter_fields = [f.name for f in UsersGroup._meta.fields + UsersGroup._meta.related_objects if
                     not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields
    serializer_class = UsersGroupSerializer

    def get_permissions(self):
        """
        Возвращает права доступа
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (Nobody,)

        return [permission() for permission in permission_classes]
