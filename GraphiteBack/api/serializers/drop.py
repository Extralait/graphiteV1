from rest_framework.exceptions import APIException
from rest_framework import serializers

from api.models import OwnerDrop, Drop, Tags
from api.serializers.intermediate import UserUserSubscriptionSerializer


class DropSerializer(UserUserSubscriptionSerializer):

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(DropSerializer, self).__init__(*args, **kwargs)

    drops_subscriptions_quantity = serializers.SerializerMethodField()
    likes_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Drop
        fields = '__all__'
        read_only_fields = ['id']

    def _is_owner(self):
        owner_drops = []

        drops = OwnerDrop.objects.all().filter(owner=self._user().id)
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

        drop.tags.set(tags)
        drop.save()

        OwnerDrop.objects.create(
            owner = self._user(),
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
            instance.url_landing = validated_data.get('url_landing', instance.url_landing)

            instance.tags.set(validated_data.get('tags', instance.tags))

            instance.save()
        return instance

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


