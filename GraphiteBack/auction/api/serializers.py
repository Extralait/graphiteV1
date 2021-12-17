from rest_framework import serializers

from auction.models import Auction, AuctionUserBid
from drops.api.serializers import DropDetailsSerializer
from users.api.serializers import UserListSerializer


class AuctionListSerializer(serializers.ModelSerializer):
    """
    Аукцион (Сериализатор)
    """
    all_bids_quantity = serializers.SerializerMethodField()
    current_user = UserListSerializer(read_only=True)
    drop = DropDetailsSerializer(read_only=True)

    def get_all_bids_quantity(self, obj):
        """
        Всего ставок
        """
        return obj.auction_user_bid.count()

    class Meta:
        model = Auction
        fields = '__all__'
        read_only_fields = ['drop', 'init_cost', 'current_cost',
                            'current_user', 'min_rate', 'sell_count',
                            'auction_deadline', 'royalty', 'is_active']


class AuctionUserBidSerializer(serializers.ModelSerializer):
    """
    Ставка на аукционе (Сериализатор)
    """
    user = UserListSerializer(read_only=True)

    class Meta:
        model = AuctionUserBid
        fields = '__all__'
        read_only_fields = ['user', 'auction', 'bid']


class PlaceBidSerializer(serializers.Serializer):
    """
    Сделать ставку на аукцмоне
    """
    bid = serializers.FloatField()