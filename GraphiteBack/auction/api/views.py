from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from auction.api.serializers import AuctionListSerializer, PlaceBidSerializer, AuctionUserBidSerializer, \
    AuctionDetailSerializer
from auction.models import Auction, AuctionUserBid
from auction.permissions import AuctionOwnerOrAdmin
from auction.services.auction_operations import place_bid, delete_bid
from utils.pagination import StandardResultsSetPagination
from utils.permissions import Nobody


class AuctionViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    Аукцион (Представление)
    """
    pagination_class = StandardResultsSetPagination
    queryset = Auction.objects.all()
    filter_fields = [f.name for f in Auction._meta.fields + Auction._meta.related_objects if
                     not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields

    def get_permissions(self):
        """
        Возвращает права доступа
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = (AllowAny,)
        elif self.action in ['place_bid', 'delete_bid',None]:
            permission_classes = (IsAuthenticated,)
        elif self.action in ['destroy']:
            permission_classes = (AuctionOwnerOrAdmin,)
        else:
            permission_classes = (Nobody,)

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Возвращает класс сериализатора
        """
        if self.action in ['place_bid']:
            serializer_class = PlaceBidSerializer
        else:
            if self.detail:
                serializer_class = AuctionDetailSerializer
            else:
                serializer_class = AuctionListSerializer

        return serializer_class

    def _is_owner(self):
        detail_auction_pk = self.kwargs.get('pk')
        if not detail_auction_pk:
            return False
        current_user_pk = self.request.user.pk
        auction_owner_pk = Auction.objects.get(drop_id=detail_auction_pk).drop.owner.pk
        return auction_owner_pk == current_user_pk

    @action(
        detail=True,
        methods=['post'],
        name='place-bid',
        url_path='place-bid',
        permission_classes=(IsAuthenticated,),
    )
    def place_bid(self, request, **kwargs):
        """
        Сделать ставку
        """
        if self._is_owner():
            return Response(
                {
                    'detail': 'It is impossible to place a bid on yourself auction'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                bid = serializer.validated_data['bid']

                return place_bid(
                    auction_id=int(self.kwargs.get('pk')),
                    user=self.request.user,
                    bid=bid
                )
            else:
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

    @place_bid.mapping.delete
    def delete_bid(self, request, **kwargs):
        """
        Удаление ставки
        """
        if self._is_owner():
            return Response(
                {
                    'detail': 'It is impossible to delete bid on yourself auction'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return delete_bid(
                auction_id=int(self.kwargs.get('pk')),
                user=self.request.user,
            )


class AuctionUserBidViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    Ставка на аукционе (Представление)
    """
    pagination_class = StandardResultsSetPagination
    queryset = AuctionUserBid.objects.all()
    filter_fields = [f.name for f in AuctionUserBid._meta.fields + AuctionUserBid._meta.related_objects if
                     not f.__dict__.get('upload_to')]
    ordering_fields = filter_fields
    serializer_class = AuctionUserBidSerializer

    def get_permissions(self):
        """
        Возвращает права доступа
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = (AllowAny,)
        else:
            permission_classes = (Nobody,)

        return [permission() for permission in permission_classes]

