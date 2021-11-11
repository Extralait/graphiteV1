from rest_framework import serializers

from api.models import ProfileType, VerifyStatus


class ProfileTypeSerializer(serializers.ModelSerializer):
    """
    тип профиля (сериализатор)
    """

    class Meta:
        model = ProfileType
        fields = ['id', 'name']
        read_only_fields = fields


class ProcessedFileSerializer(serializers.ModelSerializer):
    """
    Статус верификации (сериализатор)
    """

    class Meta:
        model = VerifyStatus
        fields = ['id', 'name']
        read_only_fields = fields
