from django.db import models


class Notification(models.Model):
    """
    Уведомления (Модель)
    """
    class NotificationType(models.TextChoices):
        """
        Тип уведомления
        """
        USER_SUBSCRIPTION = 'user_subscription', 'User subscription'
        DROP_SUBSCRIPTION = 'drop_subscription', 'Drop subscription'
        COLLECTION_SUBSCRIPTION = 'collection_subscription', 'Collection subscription'
        DROP_LIKE = 'drop_like', 'Drop like'
        COLLECTION_LIKE = 'collection_like', 'Collection like'
        USER_VIEW = 'user_view', 'User view'
        DROP_VIEW = 'drop_view', 'Drop view'
        COLLECTION_VIEW = 'collection_view', 'Collection view'
        DROP_PUT_UP_FOR_SALE = 'drop_put_up_for_sale', 'Drop put up for sale'
        DROP_BUY = 'drop_buy', 'Drop buy'
        OFFER = 'offer', 'Offer'
        CONFIRM_OFFER = 'confirm_offer', 'Confirm offer'
        NEW_DROP = 'new_drop', 'New drop'
        SYSTEM = 'system', 'System'

    notification_type = models.CharField(
        verbose_name='Notification type',
        max_length=50,
        choices=NotificationType.choices
    )
    from_user = models.ForeignKey(
        to='users.User',
        related_name='from_user_notifications',
        verbose_name='From user',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    to_user = models.ForeignKey(
        to='users.User',
        related_name='to_user_notifications',
        verbose_name='To user',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    to_drop = models.ForeignKey(
        to='drops.Drop',
        related_name='to_drop_notifications',
        verbose_name='To drop',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    to_collection = models.ForeignKey(
        to='drops_collections.Collection',
        related_name='to_collection_notifications',
        verbose_name='To collection',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    header = models.CharField(
        verbose_name='Header',
        max_length=250,
        null=True,
        blank=True,
    )
    body = models.TextField(
        verbose_name='Body',
        null=True,
        blank=True
    )
    details = models.TextField(
        verbose_name='Details',
        default='',
        blank=True
    )
    is_viewed = models.BooleanField(
        verbose_name='Is viewed',
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name='Is active',
        default=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notification'

    def save(self, *args, **kwargs):
        """
        Обработка полей перед сохранением модели
        """
        if not self.pk:
            if self.notification_type == 'user_subscription':
                self.header = 'Subscribed to your profile'
                self.body = f'{self.from_user} subscribed to your profile'

            elif self.notification_type == 'drop_subscription':
                self.header = 'Subscribed to your drop'
                self.body = f'{self.from_user} subscribed to your drop {self.to_drop}'

            elif self.notification_type == 'collection_subscription':
                self.header = 'Subscribed to your collection'
                self.body = f'{self.from_user} subscribed to your collection {self.to_collection}'

            elif self.notification_type == 'drop_like':
                self.header = 'Your drop was liked'
                self.body = f'{self.from_user} like your drop {self.to_drop}'

            elif self.notification_type == 'collection_like':
                self.header = 'Your collection was liked'
                self.body = f'{self.from_user} like your collection {self.to_collection}'

            elif self.notification_type == 'user_view':
                self.header = 'Your profile has been viewed'
                self.body = f'{self.from_user} viewed your profile'

            elif self.notification_type == 'drop_view':
                self.header = 'Your drop has been viewed'
                self.body = f'{self.from_user} viewed your drop {self.to_drop}'

            elif self.notification_type == 'collection_view':
                self.header = 'Your collection has been viewed'
                self.body = f'{self.from_user} viewed your collection {self.to_collection}'

            elif self.notification_type == 'drop_buy':
                self.header = 'Your drop was bought'

            elif self.notification_type == 'offer':
                self.header = 'Offer on your drop'

            elif self.notification_type == 'confirm_offer':
                self.header = 'Confirm your offer on drop'

            elif self.notification_type == 'new_drop':
                self.header = 'New drop in the profile to which you are subscribed'
                self.body = f'{self.from_user} posted a new drop {self.to_drop}'

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Переопределение удаления модели
        """
        self.is_active = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.from_user} - {self.to_user}: {self.notification_type}"
