from rest_framework import serializers

from transactions.models import Transaction
from users.api.serializers import UserListSerializer


class TransactionSerializer(serializers.ModelSerializer):
    """
    Транзакции (Сериализатор)
    """
    owner = UserListSerializer(read_only=True)
    buyer = UserListSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'
