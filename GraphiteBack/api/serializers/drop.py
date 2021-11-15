from rest_framework.exceptions import APIException
from rest_framework import serializers

from api.models import OwnerDrop, Drop, Tags, Categories
from api.serializers.intermediate import UserUserSubscriptionSerializer


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




class DropSerializer(UserUserSubscriptionSerializer):

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(DropSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Drop
        fields = '__all__'
        read_only_fields = ['id','all_sell_count']

    def _is_owner(self):
        owner_drops = []

        drops = OwnerDrop.objects.all().filter(drop_owner=self._user().id)
        for drop in drops:
            owner_drops.append(drop)

        return owner_drops

    def create(self, validated_data):
        """
        Создать галлерею
        """
        tags = validated_data.pop('tags', None)
        drop = (Drop.objects.create(
            **validated_data
        ))

        try:
            drop.tags.set(tags)
        except TypeError:
            drop.tags.set(Tags.objects.none())

        drop.save()

        OwnerDrop.objects.create(
            drop_owner = self._user(),
            drop = drop
        )
        return drop

    def update(self, instance, validated_data):
        """
        Обновить галлерею
        """
        if instance.id not in self._is_owner() and not self._user().is_staff:
            raise APIException("Only the owner can edit")
        else:
            instance.name = validated_data.get('name', instance.name)
            instance.descriptions = validated_data.get('descriptions', instance.descriptions)
            instance.category = validated_data.get('category', instance.category)
            instance.artists = validated_data.get('artists', instance.artists)
            instance.picture_big = validated_data.get('picture_big', instance.picture_big)
            instance.picture_small = validated_data.get('picture_small', instance.picture_small)
            instance.blockchain_type = validated_data.get('blockchain_type', instance.blockchain_type)
            instance.blockchain_address = validated_data.get('blockchain_address', instance.blockchain_address)
            instance.blockchain_identifier = validated_data.get('blockchain_identifier', instance.blockchain_identifier)
            instance.sell_type = validated_data.get('sell_type', instance.sell_type)
            instance.init_cost = validated_data.get('init_cost', instance.init_cost)
            instance.min_rate = validated_data.get('min_rate', instance.min_rate)
            instance.auction_deadline = validated_data.get('auction_deadline', instance.auction_deadline)
            instance.royalty = validated_data.get('royalty', instance.royalty)
            instance.url_landing = validated_data.get('url_landing', instance.url_landing)
            try:
                instance.tags.set(validated_data.get('tags', instance.tags))
            except TypeError:
                instance.tags.set(Tags.objects.none())

            instance.save()
        return instance


class GetDropSerializer(DropSerializer):
    tags = TagsSerializer(many=True)
    category = CategoriesSerializer()

    drops_subscriptions_quantity = serializers.SerializerMethodField()
    likes_quantity = serializers.SerializerMethodField()
    views_quantity = serializers.SerializerMethodField()
    drop_owner = serializers.SerializerMethodField()

    def get_drops_subscriptions_quantity(self, obj):
        """
        Получить количество подписок на галлереи
        """
        return obj.drops_subscriptions.count()

    def get_likes_quantity(self, obj):
        """
        Получить художников
        """
        return obj.likes.count()

    def get_views_quantity(self, obj):
        """
        Получить художников
        """
        return obj.views.count()

    def get_drop_owner(self, obj):
        """
        Получить художников
        """
        return obj.drops_owner.all()[0].pk

class BuyDropSerializer(serializers.Serializer):
    drop = serializers.IntegerField()
    count = serializers.IntegerField()