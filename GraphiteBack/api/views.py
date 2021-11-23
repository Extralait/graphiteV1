from djoser.permissions import CurrentUserOrAdmin
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Categories, Tags, Drop, UserUserSubscription, UserDropSubscription, DropLike, OwnerDrop, \
    DropView, OwnerCollection, CollectionView, CollectionLike, UserCollectionSubscription, CollectionDrop, Collection
from .serializers.collection import GetCollectionSerializer, CollectionSerializer
from .serializers.drop import DropSerializer, CategoriesSerializer, TagsSerializer, BuyDropSerializer, \
    GetDropSerializer
from .serializers.intermediate import UserUserSubscriptionSerializer, UserDropSubscriptionSerializer, \
    DropLikeSerializer, \
    OwnerDropSerializer, OwnerCollectionSerializer, CollectionViewSerializer, CollectionLikeSerializer, \
    UserCollectionSubscriptionSerializer, CollectionDropSerializer, DropViewSerializer
from .serializers.user import OtherUserDetailSerializer, OtherUserSerializer
from .services.drop_operations import sell_drop


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 1000


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 60
    page_size_query_param = 'page_size'
    max_page_size = 60


class UserProfileViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = User.objects.all()
    filter_fields = [f.name for f in User._meta.fields if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields

    def get_permissions(self):
        """
        Права доступа
        """
        if self.action in ['list', 'retrieve']:
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
        if self.action in ['list', 'retrieve']:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (IsAdminUser,)

        return [permission() for permission in permission_classes]


class TagsViewSet(CategoriesViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    filter_fields = [f.name for f in Tags._meta.fields if not f.__dict__.get('upload_to')]
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
            permission_classes = (IsAuthenticated,)

        return [permission() for permission in permission_classes]


class DropViewSet(TagsViewSet):
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

    def get_serializer_class(self):
        """
        Класс сериализатора
        """
        if self.action in ['list', 'retrieve']:
            serializer_class = GetDropSerializer
        else:
            serializer_class = DropSerializer

        return serializer_class


class CollectionViewSet(TagsViewSet):
    queryset = Collection.objects.all()
    filter_fields = [f.name for f in Collection._meta.fields if not f.__dict__.get('upload_to')]
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

    def get_serializer_class(self):
        """
        Класс сериализатора
        """
        if self.action in ['list', 'retrieve']:
            serializer_class = GetCollectionSerializer
        else:
            serializer_class = CollectionSerializer

        return serializer_class


class BuyDrop(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = BuyDropSerializer

    def post(self, request, format=None):
        """
        Return a list of all users.
        """
        data = request.data
        drop = data['drop']
        count = int(data['count'])
        user = request.user.id

        sell_count, customer, owner, customer_drop = sell_drop(drop, count, user)

        return Response({
            'owner': owner,
            'customer': customer,
            'owner_drop': drop.pk,
            'customer_drop': customer_drop,
            'sell_count': sell_count
        }, status=status.HTTP_200_OK)


class UserUserSubscriptionViewSet(TagsViewSet):
    serializer_class = UserUserSubscriptionSerializer
    queryset = UserUserSubscription.objects.all()
    filter_fields = [f.name for f in UserUserSubscription._meta.fields if not f.__dict__.get('upload_to')]
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


class UserDropSubscriptionViewSet(TagsViewSet):
    serializer_class = UserDropSubscriptionSerializer
    queryset = UserDropSubscription.objects.all()
    filter_fields = [f.name for f in UserDropSubscription._meta.fields if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields


class DropLikeViewSet(TagsViewSet):
    serializer_class = DropLikeSerializer
    queryset = DropLike.objects.all()
    filter_fields = [f.name for f in DropLike._meta.fields if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields


class DropViewViewSet(TagsViewSet):
    serializer_class = DropViewSerializer
    queryset = DropView.objects.all()
    filter_fields = [f.name for f in DropView._meta.fields if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields


class OwnerDropViewSet(TagsViewSet):
    serializer_class = OwnerDropSerializer
    queryset = OwnerDrop.objects.all()
    filter_fields = [f.name for f in OwnerDrop._meta.fields if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields


class UserCollectionSubscriptionViewSet(TagsViewSet):
    serializer_class = UserCollectionSubscriptionSerializer
    queryset = UserCollectionSubscription.objects.all()
    filter_fields = [f.name for f in UserCollectionSubscription._meta.fields if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields


class CollectionLikeViewSet(TagsViewSet):
    serializer_class = CollectionLikeSerializer
    queryset = CollectionLike.objects.all()
    filter_fields = [f.name for f in CollectionLike._meta.fields if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields


class CollectionViewViewSet(TagsViewSet):
    serializer_class = CollectionViewSerializer
    queryset = CollectionView.objects.all()
    filter_fields = [f.name for f in CollectionView._meta.fields if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields


class OwnerCollectionViewSet(TagsViewSet):
    serializer_class = OwnerCollectionSerializer
    queryset = OwnerCollection.objects.all()
    filter_fields = [f.name for f in OwnerCollection._meta.fields if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields


class CollectionDropViewSet(TagsViewSet):
    serializer_class = CollectionDropSerializer
    queryset = CollectionDrop.objects.all()
    filter_fields = [f.name for f in CollectionDrop._meta.fields if not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields
