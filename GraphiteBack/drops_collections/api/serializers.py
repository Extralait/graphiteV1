from rest_framework import serializers

from drops_collections.models import Collection
from users.api.serializers import UserListSerializer
from utils.serializers import RelationshipCheck


class StatsSerializer(serializers.ModelSerializer):
    """
    Статистика коллекции (Сериализатор)
    """
    collection_subscribers_quantity = serializers.SerializerMethodField()
    drops_subscribers_quantity = serializers.SerializerMethodField()
    collection_likes_quantity = serializers.SerializerMethodField()
    drops_likes_quantity = serializers.SerializerMethodField()
    collection_views_quantity = serializers.SerializerMethodField()
    drops_views_quantity = serializers.SerializerMethodField()
    drops_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Collection

    def get_drops_quantity(self, obj):
        """
        Получить количество коллекций
        """
        return obj.drops.count()

    def get_collection_subscribers_quantity(self, obj):
        """
        Получить количество подписчиков на коллекцию
        """
        return obj.subscribers.count()

    def get_drops_subscribers_quantity(self, obj):
        """
        Получить количество подписчиков на дропы
        """
        return sum(map(lambda x: x.subscribers.count(), obj.drops.all()))

    def get_collection_likes_quantity(self, obj):
        """
        Получить количество лайков на коллекции
        """
        return obj.likes.count()

    def get_drops_likes_quantity(self, obj):
        """
        Получить количество лайков на дропах
        """
        return sum(map(lambda x: x.likes.count(), obj.drops.all()))

    def get_collection_views_quantity(self, obj):
        """
        Получить количество просмотров коллекции
        """
        return obj.views.count()

    def get_drops_views_quantity(self, obj):
        """
        Получить количество просмотров дропов
        """
        return sum(map(lambda x: x.views.count(), obj.drops.all()))


class CollectionRelationshipCheck(RelationshipCheck):
    """
    Отношения с пользователями (Сериализатор)
    """

    class Meta:
        model = Collection


class CollectionListSerializer(CollectionRelationshipCheck):
    """
    Лист коллекций (Сериализатор)
    """
    owner = UserListSerializer(read_only=True)

    class Meta:
        model = Collection
        fields = '__all__'


class CurrentUserCollectionDetailsSerializer(StatsSerializer):
    """
    Детали коллекции для владелька (Сериализатор)
    """

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(CurrentUserCollectionDetailsSerializer, self).__init__(*args, **kwargs)

    owner = UserListSerializer(read_only=True)

    class Meta:
        model = Collection
        fields = '__all__'
        read_only_fields = ['is_active']

    def _user(self):
        """
        Получение текущего пользователя
        """
        return self.context['request'].user

    def create(self, validated_data):
        """
        Создать коллекцию
        """
        collection = (Collection.objects.create(
            owner=self._user(),
            **validated_data
        ))

        collection.save()
        return collection


class CollectionDetailsSerializer(CollectionRelationshipCheck, CurrentUserCollectionDetailsSerializer):
    """
    Детали коллекции (Сериализатор)
    """

    class Meta:
        model = Collection
        fields = '__all__'
        read_only_fields = ['is_active']



