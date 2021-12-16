import PIL.Image
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.exceptions import APIException

from auction.models import Auction
from drops.models import Category, Tag, Drop, SpecialCollectionDrop
from drops_collections.api.serializers import CollectionListSerializer
from drops_collections.models import SpecialCollection, Collection
from users.api.serializers import UserListSerializer
from utils.serializers import RelationshipCheck
from django.core.files.base import File


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


class PKTagSerializer(serializers.ModelSerializer):
    """
    Тег дропа (сериализатор)
    """

    class Meta:
        model = Tag
        fields = ['name']
        extra_kwargs = {
            'name': {'validators': []},
        }


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
    owner = UserListSerializer(read_only=True)
    artist = UserListSerializer(read_only=True)
    from_collection = CollectionListSerializer()
    current_auction_id = serializers.SerializerMethodField()
    current_auction_cost = serializers.SerializerMethodField()

    def get_current_auction_id(self, obj):
        """
        Получить id текущего аукциона
        """
        try:
            auction = obj.auction.get(is_active=True).pk
        except Auction.DoesNotExist:
            auction = None
        return auction

    def get_current_auction_cost(self, obj):
        """
        Получить текущую цену на аукционе
        """
        try:
            current_cost = obj.auction.get(is_active=True).current_cost
        except Auction.DoesNotExist:
            current_cost = None
        return current_cost

    class Meta:
        model = Drop
        fields = [
            'id', 'name', 'category', 'tags', 'artist', 'to_sell', 'sell_type',
            'owner', 'from_collection', 'parent', 'picture_big', 'picture_small',
            'is_active', 'updated_at', 'created_at', 'init_cost', 'auction_deadline',
            'current_auction_cost','current_auction_id'
        ]


class DropListSerializer(StatsSerializer, DropRelationshipCheck, BaseDropSerializer):
    """
    Лист дропов (Сериализатор)
    """
    parent = BaseDropSerializer(read_only=True)

    class Meta:
        model = Drop
        fields = [
            'id', 'subscriptions_quantity', 'likes_quantity', 'views_quantity',
            'name', 'category', 'tags', 'artist', 'to_sell', 'sell_type',
            'owner', 'from_collection', 'parent', 'picture_big', 'picture_small',
            'is_viewed', 'is_subscribed', 'is_liked', 'is_active', 'init_cost',
            'updated_at', 'created_at', 'auction_deadline','current_auction_id','current_auction_cost'
        ]


class DropCreateOrUpdateSerializer(serializers.ModelSerializer):
    """
    Создание или редактирование дропа
    """

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(DropCreateOrUpdateSerializer, self).__init__(*args, **kwargs)

    tags = PKTagSerializer(many=True)

    class Meta:
        model = Drop
        exclude = ['owner', 'artist', 'parent', 'in_stock', 'is_active']

    def _user(self):
        """
        Получение текущего пользователя
        """
        return self.context['request'].user

    def to_sell_check(self, validated_data, instance=None):
        """
        Проверка статуса продажи
        """
        to_sell = validated_data.get('to_sell', '+')
        sell_type = validated_data.get('sell_type', '+')
        sell_count = validated_data.get('sell_count', '+')
        init_cost = validated_data.get('init_cost', '+')
        min_rate = validated_data.get('min_rate', '+')
        auction_deadline = validated_data.get('auction_deadline', '+')

        errors = {'errors': []}

        if instance and instance.sell_type == 'auction' and instance.to_sell:
            royalty = validated_data.get('royalty', '+')
            if (
                to_sell != '+'
                or sell_type != '+'
                or royalty != '+'
                or auction_deadline != '+'
                or sell_count != '+'
                or init_cost != '+'
                or min_rate != '+'
            ):
                errors['errors'].append({
                    'details': 'You can`t change the  fields (to_sell, sell_type, '
                               'royalty, auction_deadline , sell_count, init_cost, '
                               'min_rate) on which the auction depends until it ends'
                })

        if to_sell:
            if sell_type == 'auction':
                if not min_rate:
                    errors['errors'].append({
                        'details': 'min_rate must be greater than 0'
                    })
            if sell_type in ["to_sell", "auction"]:
                if not sell_count:
                    errors['errors'].append({
                        'details': 'sell_count must be greater than 0'
                    })
                if not init_cost:
                    errors['errors'].append({
                        'details': 'init_cost must be greater than 0'
                    })
            else:
                errors['errors'].append({
                    'details': 'sell_type must be "auction" or "to_sell"'
                })

        return errors

    def create(self, validated_data):
        """
        Создать дроп
        """

        from_collection = validated_data.pop('from_collection', None)
        validated_data.pop('csrfmiddlewaretoken', None)

        if from_collection and not self._user().collections.filter(pk=int(from_collection)).count():
            raise APIException(f'You are not the owner of collection "{from_collection}"')

        data = {
            'owner': self._user(),
            'artist': self._user()
        }
        if from_collection:
            data['from_collection_id'] = int(from_collection)

        to_sell_errors = self.to_sell_check(validated_data)

        if len(to_sell_errors['errors']):
            raise APIException(to_sell_errors)

        tags = validated_data.pop('tags', None)
        # self.create_or_get_tags(tags)
        drop = (Drop.objects.create(
            **data,
            **validated_data
        ))

        if 'included_images' in self.context:  # checking if key is in context
            images_data = self.context['included_images']
            for field_name, image in images_data.items():
                getattr(drop, field_name).save(image.name, File(image))

        # print(tags)
        if tags:
            for tag in tags:
                # print(tag)
                tag, create = Tag.objects.get_or_create(name=tag['name'])
                drop.tags.add(tag)

        drop.save()
        return drop

    def update(self, instance, validated_data):
        """
        Обновить дроп
        """
        from_collection = validated_data.pop('from_collection', None)
        validated_data.pop('csrfmiddlewaretoken', None)
        if from_collection:
            validated_data['from_collection_id'] = int(from_collection)

        if from_collection and not self._user().collections.filter(pk=int(from_collection)).count():
            raise APIException(f'You are not the owner of collection "{from_collection}"')

        to_sell_errors = self.to_sell_check(validated_data, instance)

        if len(to_sell_errors['errors']):
            raise APIException(to_sell_errors)

        instance.sell_type = validated_data.get('sell_type', instance.sell_type)
        instance.sell_count = validated_data.get('sell_count', instance.sell_count)
        instance.to_sell = validated_data.get('to_sell', instance.to_sell)
        instance.init_cost = validated_data.get('init_cost', instance.init_cost)
        instance.min_rate = validated_data.get('min_rate', instance.min_rate)
        instance.auction_deadline = validated_data.get('auction_deadline', instance.auction_deadline)
        instance.from_collection_id = validated_data.get('from_collection_id', instance.from_collection_id)
        if not instance.parent:
            instance.name = validated_data.get('name', instance.name)
            instance.descriptions = validated_data.get('descriptions', instance.descriptions)
            instance.category = validated_data.get('category', instance.category)

            if 'included_images' in self.context:  # checking if key is in context
                images_data = self.context['included_images']
                for field_name, image in images_data.items():
                    getattr(instance, field_name).save(image.name, File(image))

            # instance.blockchain_type = validated_data.get('blockchain_type', instance.blockchain_type)
            # instance.blockchain_address = validated_data.get('blockchain_address', instance.blockchain_address)
            # instance.blockchain_identifier = validated_data.get('blockchain_identifier', instance.blockchain_identifier)
            instance.url_landing = validated_data.get('url_landing', instance.url_landing)
            instance.specifications = validated_data.get('specifications', instance.specifications)
            instance.royalty = validated_data.get('royalty', instance.royalty)

            tags = validated_data.pop('tags', instance.tags)
            instance_tags = instance.tags.all()
            if tags != instance.tags:
                if tags:
                    instance.tags.set(Tag.objects.none())
                    for tag in tags:
                        tag, create = Tag.objects.get_or_create(name=tag['name'])
                        if tag not in instance_tags:
                            instance.tags.add(tag)
                else:
                    instance.tags.set(Tag.objects.none())

        instance.save()
        return instance


class DropDetailsSerializer(DropRelationshipCheck, StatsSerializer, BaseDropSerializer):
    """
    Детали дропа (Сериализатор)
    """
    parent = DropListSerializer(read_only=True)

    size = serializers.SerializerMethodField()
    height = serializers.SerializerMethodField()
    width = serializers.SerializerMethodField()

    def get_size(self, obj):
        """
        Получить размер
        """
        return obj.picture_big.size if obj.picture_big else None

    def get_height(self, obj):
        """
        Получить высоту
        """
        if obj.picture_big:
            img = PIL.Image.open(obj.picture_big.path)
            return img.height
        else:
            return None

    def get_width(self, obj):
        """
        Получить ширину
        """
        if obj.picture_big:
            img = PIL.Image.open(obj.picture_big.path)
            return img.width
        else:
            return None

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
