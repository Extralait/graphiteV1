from rest_framework import serializers
from rest_framework.exceptions import APIException

from api.models import UserUserSubscription, UserDropSubscription, DropLike, OwnerDrop, DropView, CollectionLike, \
    CollectionView, OwnerCollection, UserCollectionSubscription, CollectionDrop


class UserUserSubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserUserSubscription
        fields = '__all__'
        read_only_fields = ['id','current_user']

    def _user(self):
        """
        Получение пользователя
        """
        user = self.context['request'].user
        return user

    def create(self, validated_data):
        """
        Подписаться
        """
        user_user_subscription = (UserUserSubscription.objects.create(
            current_user=self._user(),
            **validated_data
        ))
        return user_user_subscription


class CollectionDropSerializer(serializers.ModelSerializer):

    class Meta:
        model = CollectionDrop
        fields = '__all__'
        read_only_fields = ['id']

    def _user(self):
        """
        Получение пользователя
        """
        user = self.context['request'].user
        return user
    
    def _is_owner(self):
        owner_collections = []

        collections = OwnerCollection.objects.all().filter(collection_owner=self._user().id)
        for collection in collections:
            owner_collections.append(collection.pk)

        return owner_collections

    def create(self, validated_data):
        """
        Подписаться
        """
        print(self._is_owner())
        print(validated_data.get('drop_collection'))
        if validated_data.get('drop_collection').pk not in self._is_owner():
            raise APIException("Only the owner can edit")

        collection_drop = (CollectionDrop.objects.create(
            **validated_data
        ))
        return collection_drop


class UserDropSubscriptionSerializer(UserUserSubscriptionSerializer):

    class Meta:
        model = UserDropSubscription
        fields = '__all__'
        read_only_fields = ['id','subscriber']

    def create(self, validated_data):
        """
        Подписаться
        """
        user_drop_subscription = (UserDropSubscription.objects.create(
            subscriber=self._user(),
            **validated_data
        ))
        return user_drop_subscription


class UserCollectionSubscriptionSerializer(UserUserSubscriptionSerializer):

    class Meta:
        model = UserCollectionSubscription
        fields = '__all__'
        read_only_fields = ['id','subscriber']

    def create(self, validated_data):
        """
        Подписаться
        """
        user_collection_subscription = (UserCollectionSubscription.objects.create(
            subscriber=self._user(),
            **validated_data
        ))
        return user_collection_subscription


class DropLikeSerializer(UserUserSubscriptionSerializer):

    class Meta:
        model = DropLike
        fields = '__all__'
        read_only_fields = ['id','user']

    def create(self, validated_data):
        """
        Стать художником
        """
        like = (DropLike.objects.create(
            user=self._user(),
            **validated_data
        ))
        return like


class CollectionLikeSerializer(UserUserSubscriptionSerializer):

    class Meta:
        model = CollectionLike
        fields = '__all__'
        read_only_fields = ['id','user']

    def create(self, validated_data):
        """
        Стать художником
        """
        like = (CollectionLike.objects.create(
            user=self._user(),
            **validated_data
        ))
        return like


class DropViewSerializer(UserUserSubscriptionSerializer):

    class Meta:
        model = DropView
        fields = '__all__'
        read_only_fields = ['id','user']

    def create(self, validated_data):
        """
        Стать художником
        """
        view = (DropView.objects.create(
            user=self._user(),
            **validated_data
        ))
        return view


class CollectionViewSerializer(UserUserSubscriptionSerializer):

    class Meta:
        model = CollectionView
        fields = '__all__'
        read_only_fields = ['id','user']

    def create(self, validated_data):
        """
        Стать художником
        """
        view = (CollectionView.objects.create(
            user=self._user(),
            **validated_data
        ))
        return view


class OwnerDropSerializer(UserUserSubscriptionSerializer):

    class Meta:
        model = OwnerDrop
        fields = '__all__'
        read_only_fields = ['id','owner','drop']


class OwnerCollectionSerializer(UserUserSubscriptionSerializer):

    class Meta:
        model = OwnerCollection
        fields = '__all__'
        read_only_fields = ['id','collection_owner','collection']



