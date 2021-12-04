from django.db.models import Model
from rest_framework import serializers


class RelationshipCheck(serializers.ModelSerializer):
    """
    Отношения с пользователями (Сериализатор)
    """
    is_subscribed = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_viewed = serializers.SerializerMethodField()

    def _user(self):
        """
        Получение текущего пользователя
        """
        return self.context['request'].user

    class Meta:
        model = Model

    def get_is_subscribed(self, obj):
        """
        Получить наличие подписки
        """
        return bool(obj.subscribers.filter(pk=self._user().pk).count())

    def get_is_liked(self, obj):
        """
        Получить наличие лайка
        """
        return bool(obj.likes.filter(pk=self._user().pk).count())

    def get_is_viewed(self, obj):
        """
        Получить наличие просмотра
        """
        return bool(obj.views.filter(pk=self._user().pk).count())
