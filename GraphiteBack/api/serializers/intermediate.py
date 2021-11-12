from rest_framework import serializers

from api.models import UserUserSubscription, UserDropSubscription, Like


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


class LikeSerializer(UserUserSubscriptionSerializer):

    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ['id','user']

    def create(self, validated_data):
        """
        Стать художником
        """
        like = (Like.objects.create(
            user=self._user(),
            **validated_data
        ))
        return like


