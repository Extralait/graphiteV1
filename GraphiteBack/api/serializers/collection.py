from rest_framework import serializers
from rest_framework.exceptions import APIException

from api.models import Collection, OwnerDrop, OwnerCollection, Drop
from api.serializers.intermediate import UserUserSubscriptionSerializer


class CollectionSerializer(UserUserSubscriptionSerializer):

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(CollectionSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Collection
        fields = '__all__'
        read_only_fields = ['id']

    def _is_owner(self):
        owner_collections = []

        collections = OwnerCollection.objects.all().filter(collection_owner=self._user().id)
        for collection in collections:
            owner_collections.append(collection)
        print(collections)
        return owner_collections

    def create(self, validated_data):
        """
        Создать коллекцию
        """
        # tags = validated_data.pop('tags', None)
        collection = (Collection.objects.create(
            **validated_data
        ))

        # try:
        #     drop.tags.set(tags)
        # except TypeError:
        #     drop.tags.set(Tags.objects.none())

        collection.save()

        OwnerCollection.objects.create(
            collection_owner = self._user(),
            collection = collection
        )
        return collection

    def update(self, instance, validated_data):
        """
        Обновить коллекцию
        """
        if instance.id not in self._is_owner() and not self._user().is_staff:
            raise APIException("Only the owner can edit")
        else:
            instance.name = validated_data.get('name', instance.name)
            try:
                instance.tags.set(validated_data.get('drops', instance.tags))
            except TypeError:
                instance.tags.set(Drop.objects.none())

            instance.save()
        return instance


class GetCollectionSerializer(CollectionSerializer):

    collection_subscriptions_quantity = serializers.SerializerMethodField()
    likes_quantity = serializers.SerializerMethodField()
    views_quantity = serializers.SerializerMethodField()
    collection_owner = serializers.SerializerMethodField()
    subscribers_on_own_drops_quantity = serializers.SerializerMethodField()
    own_drop_views_quantity = serializers.SerializerMethodField()
    own_drop_likes_quantity = serializers.SerializerMethodField()


    def get_collection_subscriptions_quantity(self, obj):
        """
        Получить количество подписок на коллекцию
        """
        return obj.collections_subscriptions.count()

    def get_subscribers_on_own_drops_quantity(self, obj):
        """
        Получить количество подписчиков
        """
        return sum(map(lambda x: x.drops_subscriptions.all().count(), obj.drops.all()))

    def get_own_drop_likes_quantity(self, obj):
        """
        Получить количество подписчиков
        """
        return sum(map(lambda x: x.drop_likes.all().count(), obj.drops.all()))

    def get_own_drop_views_quantity(self, obj):
        """
        Получить количество подписчиков
        """
        return sum(map(lambda x: x.drop_views.all().count(), obj.drops.all()))

    def get_likes_quantity(self, obj):
        """
        Получить художников
        """
        return obj.collection_likes.count()

    def get_views_quantity(self, obj):
        """
        Получить художников
        """
        return obj.collection_views.count()

    def get_collection_owner(self, obj):
        """
        Получить художников
        """
        return obj.user_collections.all()[0].pk

