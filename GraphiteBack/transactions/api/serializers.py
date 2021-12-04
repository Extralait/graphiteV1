from rest_framework import serializers

from transactions.models import Transaction
from users.api.serializers import UserListSerializer


class TransactionSerializer(serializers.ModelSerializer):
    """
    Транзакции (Сериализатор)
    """

    class Meta:
        model = Transaction
        fields = '__all__'
