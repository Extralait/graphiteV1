from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from djoser.permissions import CurrentUserOrAdmin

from api.permissions import NoBody
from .models import User, Categories, Tags, Drop, UserUserSubscription, UserDropSubscription, Like
from .serializers.common import CategoriesSerializer, TagsSerializer
from .serializers.drop import DropSerializer
from .serializers.intermediate import UserUserSubscriptionSerializer, UserDropSubscriptionSerializer, LikeSerializer
from .serializers.user import OtherUserDetailSerializer, OtherUserSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 1000



class SmallResultsSetPagination(PageNumberPagination):
    page_size = 60
    page_size_query_param = 'page_size'
    max_page_size = 60

    # def get_permissions(self):
    #     """
    #     Права доступа
    #     """
    #     if self.action in ['create']:
    #         permission_classes = (IsAuthenticated,)
    #     elif self.action in ['destroy']:
    #         permission_classes = (IsAdminUser,)
    #     elif self.action in ['update', 'partial_update']:
    #         permission_classes = (IsLeaderOrAdmin,)
    #     else:
    #         permission_classes = (AllowAny,)
    #
    #     return [permission() for permission in permission_classes]
    #
    # def get_serializer_class(self):
    #     """
    #     Класс сериализатора
    #     """
    #     if self.request.user.is_staff:
    #         serializer_class = OrganizationAdminSerializer
    #     else:
    #         serializer_class = OrganizationSerializer
    #
    #     return serializer_class



class UserProfileViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = User.objects.all()
    filter_fields = [f.name for f in User._meta.fields if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields

    def get_permissions(self):
        """
        Права доступа
        """
        if self.action in ['list','retrieve']:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (CurrentUserOrAdmin,)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Класс сериализатора
        """
        if self.detail:
            serializer_class = OtherUserDetailSerializer
        else:
            serializer_class = OtherUserSerializer

        return serializer_class


class CategoriesViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_fields = [f.name for f in Categories._meta.fields if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields

    def get_permissions(self):
        """
        Права доступа
        """
        if self.action in ['list','retrieve']:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAdminUser,)

        return [permission() for permission in permission_classes]


class TagsViewSet(CategoriesViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    filter_fields = [f.name for f in Tags._meta.fields if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields



class DropViewSet(CategoriesViewSet):
    serializer_class = DropSerializer
    queryset = Drop.objects.all()
    filter_fields = [f.name for f in Drop._meta.fields if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields

    def get_permissions(self):
        """
        Права доступа
        """

        if self.action in ['list', 'retrieve']:
            permission_classes = (AllowAny,)
        elif self.action == 'create':
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (CurrentUserOrAdmin,)

        return [permission() for permission in permission_classes]


class UserUserSubscriptionViewSet(DropViewSet):
    serializer_class = UserUserSubscriptionSerializer
    queryset = UserUserSubscription.objects.all()
    filter_fields = [f.name for f in UserUserSubscription._meta.fields if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields


class UserDropSubscriptionViewSet(DropViewSet):
    serializer_class = UserDropSubscriptionSerializer
    queryset = UserDropSubscription.objects.all()
    filter_fields = [f.name for f in UserDropSubscription._meta.fields if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields

class LikeViewSet(DropViewSet):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    filter_fields = [f.name for f in Like._meta.fields if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields






