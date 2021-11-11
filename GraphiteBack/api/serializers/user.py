from rest_framework import serializers

from api.models import User


class StatsSerializer(serializers.ModelSerializer):
    subscribers_quantity = serializers.SerializerMethodField()
    subscribers_on_own_galleries_quantity = serializers.SerializerMethodField()
    users_subscriptions_quantity = serializers.SerializerMethodField()
    galleries_subscriptions_quantity = serializers.SerializerMethodField()

    class Meta:
        model = User

    def get_subscribers_quantity(self, obj):
        """
        Получить количество подписчиков
        """
        return obj.user_users_subscriptions.count()

    def get_subscribers_on_own_galleries_quantity(self, obj):
        """
        Получить количество подписчиков
        """
        return sum(map(lambda x: x.galleries_subscriptions_set.count(), obj.galleries.all()))

    def get_users_subscriptions_quantity(self, obj):
        """
        Получить количество подписок на пользователей
        """
        return obj.users_subscriptions.count()

    def get_galleries_subscriptions_quantity(self, obj):
        """
        Получить количество подписок на галлереи
        """
        return obj.galleries_subscriptions.count()


class CurrentUserSerializer(StatsSerializer):
    """
    Детали текущего пользователя (сериализатор)
    """
    class Meta:
        model = User
        exclude = ['password', 'galleries', 'users_subscriptions',
                   'galleries_subscriptions']

        read_only_fields = ['last_login','wallet_number'
                            'date_joined','owner_key']

    def update(self, instance, validated_data):

        if instance.is_superuser or instance.is_staff:
            instance.is_active = validated_data.get('is_active', instance.is_active)
            instance.is_verify = validated_data.get('is_verify', instance.is_verify)
            instance.verify_status = validated_data.get('verify_status', instance.verify_status)

        if instance.is_superuser:
            instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
            instance.is_staff = validated_data.get('is_staff', instance.is_staff)
            instance.user_permissions = validated_data.get('user_permissions', instance.user_permissions)
            instance.groups = validated_data.get('groups', instance.groups)

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.cover = validated_data.get('cover', instance.cover)
        instance.email_notification = validated_data.get('email_notification', instance.email_notification)
        instance.description = validated_data.get('description', instance.description)
        instance.instagram = validated_data.get('instagram', instance.instagram)
        instance.twitter = validated_data.get('twitter', instance.twitter)
        instance.discord = validated_data.get('discord', instance.discord)
        instance.tiktok = validated_data.get('tiktok', instance.tiktok)
        instance.telegram = validated_data.get('telegram', instance.telegram)
        instance.profile_type = validated_data.get('profile_type', instance.profile_type)

        instance.save()
        return instance


class OtherUserSerializer(CurrentUserSerializer):

    class Meta:
        model = User
        exclude = ['password', 'galleries', 'users_subscriptions',
                   'galleries_subscriptions','owner_key','wallet_number']

        read_only_fields = ['last_login','wallet_number'
                            'date_joined','owner_key']


