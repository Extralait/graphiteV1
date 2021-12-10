from rest_framework import serializers

from offers.models import Offer
from users.api.serializers import BaseUserListSerializer


class OfferSerializer(serializers.ModelSerializer):
    """
    Предложение для владельца дропа
    """
    owner = BaseUserListSerializer(read_only=True)
    buyer = BaseUserListSerializer(read_only=True)

    class Meta:
        model = Offer
        fields = '__all__'

