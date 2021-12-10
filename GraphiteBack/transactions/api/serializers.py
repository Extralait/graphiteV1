from rest_framework import serializers

from transactions.models import Transaction
from users.api.serializers import BaseUserListSerializer


class TransactionSerializer(serializers.ModelSerializer):
    """
    Транзакции (Сериализатор)
    """
    owner = BaseUserListSerializer(read_only=True)
    buyer = BaseUserListSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'
