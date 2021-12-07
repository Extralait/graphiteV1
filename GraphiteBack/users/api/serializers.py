from django.contrib.auth.models import Permission, Group
from rest_framework import serializers

from users.models import User, PassportData
from utils.serializers import RelationshipCheck


class PassportDataSerializer(serializers.ModelSerializer):
    """
    Паспортные данные (Сериализатор)
    """
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(PassportDataSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = PassportData
        fields = '__all__'
        read_only_fields = [
            'verify_status'
        ]

    def update(self, instance, validated_data):
        """
        Переопределение обновления паспорта пользователя
        """
        if instance.is_staff:
            instance.verify_status = validated_data.get('verify_status', instance.verify_status)

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.passport_series = validated_data.get('passport_series', instance.passport_series)
        instance.passport_number = validated_data.get('passport_number', instance.passport_number)
        instance.passport_issue_date = validated_data.get('passport_issue_date', instance.passport_issue_date)
        instance.passport_expiration_date = validated_data.get('passport_expiration_date', instance.passport_expiration_date)

class StatsSerializer(serializers.ModelSerializer):
    """
    Статистика пользователя (Сериализатор)
    """
    drops_in_possession_quantity = serializers.SerializerMethodField()
    drops_in_authorship_quantity = serializers.SerializerMethodField()
    collections_in_possession_quantity = serializers.SerializerMethodField()

    users_subscriptions_quantity = serializers.SerializerMethodField()
    drops_subscriptions_quantity = serializers.SerializerMethodField()
    collections_subscriptions_quantity = serializers.SerializerMethodField()

    user_subscribers_quantity = serializers.SerializerMethodField()
    drops_in_possession_subscribers_quantity = serializers.SerializerMethodField()
    drops_in_authorship_subscribers_quantity = serializers.SerializerMethodField()
    collections_subscribers_quantity = serializers.SerializerMethodField()

    drops_in_possession_likes_quantity = serializers.SerializerMethodField()
    drops_in_authorship_likes_quantity = serializers.SerializerMethodField()
    collections_likes_quantity = serializers.SerializerMethodField()

    users_views_quantity = serializers.SerializerMethodField()
    drops_in_possession_views_quantity = serializers.SerializerMethodField()
    drops_in_authorship_views_quantity = serializers.SerializerMethodField()
    collections_views_quantity = serializers.SerializerMethodField()

    all_notifications_quantity = serializers.SerializerMethodField()
    unseen_notifications_quantity = serializers.SerializerMethodField()

    class Meta:
        model = User

    def get_drops_in_possession_quantity(self, obj):
        """
        Получить количество дропов во владении
        """
        return obj.owners_drops.count()

    def get_drops_in_authorship_quantity(self, obj):
        """
        Получить количество дропов под авторством
        """
        return obj.artists_drops.count()

    def get_collections_in_possession_quantity(self, obj):
        """
        Получить коллекций
        """
        return obj.collections.count()

    def get_user_subscribers_quantity(self, obj):
        """
        Получить количество подписчиков на профиль
        """
        return obj.subscribers.count()

    def get_drops_in_possession_subscribers_quantity(self, obj):
        """
        Получить количество подписчиков на дропы во владении
        """
        return sum(map(lambda x: x.subscribers.count(), obj.owners_drops.all()))

    def get_drops_in_authorship_subscribers_quantity(self, obj):
        """
        Получить количество подписчиков на дропы под авторством
        """
        return sum(map(lambda x: x.subscribers.count(), obj.artists_drops.all()))

    def get_collections_subscribers_quantity(self, obj):
        """
        Получить количество подписчиков на коллекции
        """
        return sum(map(lambda x: x.subscribers.count(), obj.collections.all()))

    def get_drops_in_possession_likes_quantity(self, obj):
        """
        Получить количество лайков на дропах во владении
        """
        return sum(map(lambda x: x.likes.count(), obj.owners_drops.all()))

    def get_drops_in_authorship_likes_quantity(self, obj):
        """
        Получить количество лайков на дропах под авторством
        """
        return sum(map(lambda x: x.likes.count(), obj.artists_drops.all()))

    def get_collections_likes_quantity(self, obj):
        """
        Получить количество лайков на коллекциях
        """
        return sum(map(lambda x: x.likes.count(), obj.collections.all()))

    def get_users_views_quantity(self, obj):
        """
        Получить количество просмотров профиля
        """
        return obj.views.count()

    def get_drops_in_possession_views_quantity(self, obj):
        """
        Получить количество просмотров на дропах во владении
        """
        return sum(map(lambda x: x.views.count(), obj.owners_drops.all()))

    def get_drops_in_authorship_views_quantity(self, obj):
        """
        Получить количество просмотров на дропах под авторством
        """
        return sum(map(lambda x: x.views.count(), obj.artists_drops.all()))

    def get_collections_views_quantity(self, obj):
        """
        Получить количество просмотров на коллекциях
        """
        return sum(map(lambda x: x.views.count(), obj.collections.all()))

    def get_users_subscriptions_quantity(self, obj):
        """
        Получить количество подписок на пользователей
        """
        return obj.user_subscriptions.count()

    def get_drops_subscriptions_quantity(self, obj):
        """
        Получить количество подписок на дропы
        """
        return obj.drop_subscriptions.count()

    def get_collections_subscriptions_quantity(self, obj):
        """
        Получить количество подписок на коллекции
        """
        return obj.collection_subscriptions.count()

    def get_all_notifications_quantity(self, obj):
        """
        Получить общее количество уведомлений
        """
        return obj.to_user_notifications.count()

    def get_unseen_notifications_quantity(self, obj):
        """
        Получить количество непрочитанных уведомлений
        """
        return obj.to_user_notifications.filter(is_viewed=False).count()


class ShortStatsSerializer(serializers.ModelSerializer):
    """
    Короткая статистика пользователя (Сериализатор)
    """
    drops_in_possession_quantity = serializers.SerializerMethodField()
    collections_in_possession_quantity = serializers.SerializerMethodField()
    user_subscribers_quantity = serializers.SerializerMethodField()
    users_views_quantity = serializers.SerializerMethodField()

    class Meta:
        model = User

    def get_drops_in_possession_quantity(self, obj):
        """
        Получить количество дропов во владении
        """
        return obj.owners_drops.count()

    def get_collections_in_possession_quantity(self, obj):
        """
        Получить количество коллекций
        """
        return obj.collections.count()

    def get_user_subscribers_quantity(self, obj):
        """
        Получить количество подписчиков на профиль
        """
        return obj.subscribers.count()

    def get_users_views_quantity(self, obj):
        """
        Получить количество просмотров профиля
        """
        return obj.views.count()


class UserRelationshipCheck(RelationshipCheck):
    """
    Отношения между пользователями (Сериализатор)
    """
    is_liked = None
    get_is_liked = None

    class Meta:
        model = User


class UserListSerializer(ShortStatsSerializer,UserRelationshipCheck):
    """
    Лист пользователей (Сериализатор)
    """
    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name',
            'drops_in_possession_quantity', 'collections_in_possession_quantity',
            'user_subscribers_quantity', 'users_views_quantity',
            'avatar', 'wallet_number', 'instagram',
            'twitter', 'discord', 'telegram','website', 'profile_type',
            'is_viewed','is_subscribed','last_login','date_joined','updated_at'
        ]


class CurrentUserDetailsSerializer(StatsSerializer):
    """
    Детали текущего пользователя (сериализатор)
    """
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(CurrentUserDetailsSerializer, self).__init__(*args, **kwargs)

    passport_data = PassportDataSerializer(read_only=True)

    class Meta:
        model = User
        exclude = [
            'user_subscriptions', 'drop_subscriptions',
            'collection_subscriptions', 'drop_likes',
            'collections_likes', 'drop_views','user_views',
            'collections_views', 'password', 'owner_key'
        ]
        read_only_fields = [
            'last_login', 'wallet_number', 'date_joined'
        ]

    def update(self, instance, validated_data):
        """
        Переопределение обновления пользователя
        """
        if instance.is_superuser or instance.is_staff:
            instance.is_active = validated_data.get('is_active', instance.is_active)
            instance.is_verify = validated_data.get('is_verify', instance.is_verify)
            instance.verify_status = validated_data.get('verify_status', instance.verify_status)

        if instance.is_superuser:
            instance.is_superuser = validated_data.get('is_superuser', instance.is_superuser)
            instance.is_staff = validated_data.get('is_staff', instance.is_staff)
            try:
                instance.user_permissions.set(validated_data.get('user_permissions', instance.user_permissions))
            except TypeError:
                instance.user_permissions.set(Permission.objects.none())
            try:
                instance.groups.set(validated_data.get('groups', instance.groups))
            except TypeError:
                instance.groups.set(Group.objects.none())

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.cover = validated_data.get('cover', instance.cover)
        instance.inn = validated_data.get('inn', instance.inn)
        instance.website = validated_data.get('website', instance.website)
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


class UserDetailsSerializer(UserRelationshipCheck, CurrentUserDetailsSerializer):
    """
    Детали пользователя (Сериализатор)
    """
    passport_data = None

    class Meta:
        model = User
        exclude = [
            'password', 'owner_key', 'user_subscriptions',
            'drop_subscriptions', 'collection_subscriptions',
            'drop_likes', 'collections_likes', 'drop_views',
            'collections_views','user_views',
        ]
        read_only_fields = [
            'last_login', 'wallet_number', 'date_joined'
        ]

