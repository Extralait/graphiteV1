from rest_framework import serializers
from rest_framework.exceptions import APIException

from drops.models import Category, Tag, Drop, SpecialCollectionDrop
from drops_collections.api.serializers import CollectionListSerializer
from drops_collections.models import SpecialCollection
from users.api.serializers import UserListSerializer
from utils.serializers import RelationshipCheck


class CategorySerializer(serializers.ModelSerializer):
    """
    Категория дропа (сериализатор)
    """

    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """
    Тег дропа (сериализатор)
    """

    class Meta:
        model = Tag
        fields = '__all__'


class StatsSerializer(serializers.ModelSerializer):
    """
    Статистика дропа (Сериализатор)
    """
    subscriptions_quantity = serializers.SerializerMethodField()
    likes_quantity = serializers.SerializerMethodField()
    views_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Drop

    def get_subscriptions_quantity(self, obj):
        """
        Получить количество подписок на дроп
        """
        return obj.subscribers.count()

    def get_likes_quantity(self, obj):
        """
        Получить количество лайков дропа
        """
        return obj.likes.count()

    def get_views_quantity(self, obj):
        """
        Получить просмотров дропа
        """
        return obj.views.count()


class DropRelationshipCheck(RelationshipCheck):
    """
    Отношения с пользователями (Сериализатор)
    """

    class Meta:
        model = Drop
        fields = '__all__'


class BaseDropSerializer(serializers.ModelSerializer):
    """
    Базовый класс дропа (Сериализатор)
    """
    category = CategorySerializer()
    owner = UserListSerializer(read_only=True)
    artist = UserListSerializer(read_only=True)
    from_collection = CollectionListSerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Drop
        fields = [
            'id', 'name', 'category','tags', 'artist',
            'owner', 'from_collection', 'parent', 'picture_big', 'picture_small',
            'is_viewed', 'is_subscribed', 'is_liked',
            'updated_at', 'created_at'
        ]


class DropListSerializer(DropRelationshipCheck, BaseDropSerializer):
    """
    Лист дропов (Сериализатор)
    """
    parent = BaseDropSerializer(read_only=True)

    class Meta:
        model = Drop
        fields = [
            'id', 'name', 'category','tags', 'artist',
            'owner', 'from_collection', 'parent', 'picture_big', 'picture_small',
            'is_viewed', 'is_subscribed', 'is_liked',
            'updated_at', 'created_at'
        ]


class DropCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    Создание или редактирование дропа
    """

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(DropCreateOrUpdateSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Drop
        exclude = ['is_active', 'owner', 'artist']
        read_only_fields = ['in_stock', 'is_active']

    def _user(self):
        """
        Получение текущего пользователя
        """
        return self.context['request'].user

    def create(self, validated_data):
        """
        Создать дроп
        """
        tags = validated_data.pop('tags', None)
        from_collection = validated_data.get('from_collection', None)

        if from_collection and not self._user().collections.filter(pk=from_collection.pk).count():
            raise APIException(f'You are not the owner of collection "{from_collection.name}"')

        drop = (Drop.objects.create(
            owner=self._user(),
            artist=self._user(),
            **validated_data
        ))

        try:
            drop.tags.set(tags)
        except TypeError:
            drop.tags.set(Tag.objects.none())

        drop.save()
        return drop

    def update(self, instance, validated_data):
        """
        Обновить дроп
        """
        from_collection = validated_data.get('from_collection', None)

        if from_collection and not self._user().collections.filter(pk=from_collection.pk).count():
            raise APIException(f'You are not the owner of collection "{from_collection.name}"')

        instance.sell_type = validated_data.get('sell_type', instance.sell_type)
        instance.sell_count = validated_data.get('sell_count', instance.sell_count)
        instance.to_sell = validated_data.get('to_sell', instance.to_sell)
        instance.init_cost = validated_data.get('init_cost', instance.init_cost)
        instance.min_rate = validated_data.get('min_rate', instance.min_rate)
        instance.auction_deadline = validated_data.get('auction_deadline', instance.auction_deadline)
        instance.from_collection = validated_data.get('from_collection', instance.from_collection)
        if not instance.parent:
            instance.name = validated_data.get('name', instance.name)
            instance.descriptions = validated_data.get('descriptions', instance.descriptions)
            instance.category = validated_data.get('category', instance.category)
            instance.picture_big = validated_data.get('picture_big', instance.picture_big)
            instance.picture_small = validated_data.get('picture_small', instance.picture_small)
            instance.blockchain_type = validated_data.get('blockchain_type', instance.blockchain_type)
            instance.blockchain_address = validated_data.get('blockchain_address', instance.blockchain_address)
            instance.blockchain_identifier = validated_data.get('blockchain_identifier', instance.blockchain_identifier)
            instance.url_landing = validated_data.get('url_landing', instance.url_landing)
            instance.specifications = validated_data.get('specifications', instance.specifications)
            instance.royalty = validated_data.get('royalty', instance.royalty)
        try:
            instance.tags.set(validated_data.get('tags', instance.tags))
        except TypeError:
            instance.tags.set(Tag.objects.none())

        instance.save()
        return instance


class DropDetailsSerializer(DropRelationshipCheck, StatsSerializer, BaseDropSerializer):
    """
    Детали дропа (Сериализатор)
    """
    parent = DropListSerializer(read_only=True)

    class Meta:
        model = Drop
        fields = '__all__'


class DropBuySerializer(serializers.Serializer):
    """
    Покупка дропа (Сериализатор)
    """
    count = serializers.IntegerField()


class MakeOfferSerializer(serializers.Serializer):
    """
    Покупка дропа (Сериализатор)
    """
    count = serializers.IntegerField()
    unit_price = serializers.FloatField()


class SpecialCollectionDropSerializer(serializers.ModelSerializer):
    drop = DropDetailsSerializer(read_only=True)

    class Meta:
        model = SpecialCollectionDrop
        fields = ['drop', 'level']


class SpecialCollectionSerializer(serializers.ModelSerializer):
    """
    Специальные коллекции (Сериализатор)
    """
    drops = SpecialCollectionDropSerializer(read_only=True, many=True, source='special_collection_drop')

    class Meta:
        model = SpecialCollection
        fields = '__all__'
