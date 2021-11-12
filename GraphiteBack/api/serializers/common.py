from rest_framework import serializers

from api.models import Categories, Tags


class CategoriesSerializer(serializers.ModelSerializer):
    """
    тип профиля (сериализатор)
    """

    class Meta:
        model = Categories
        fields = ['id', 'name']


class TagsSerializer(serializers.ModelSerializer):
    """
    Статус верификации (сериализатор)
    """

    class Meta:
        model = Tags
        fields = ['id', 'name']
