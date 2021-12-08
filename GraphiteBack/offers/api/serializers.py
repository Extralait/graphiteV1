from rest_framework import serializers

from offers.models import Offer
from users.api.serializers import UserListSerializer


class OfferSerializer(serializers.ModelSerializer):
    """
    Предложение для владельца дропа
    """
    owner = UserListSerializer(read_only=True)
    buyer = UserListSerializer(read_only=True)

    class Meta:
        model = Offer
        fields = '__all__'

