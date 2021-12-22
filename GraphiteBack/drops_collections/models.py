from django.db import models


class Collection(models.Model):
    """
    Коллекция (Модель)
    """
    name = models.CharField(
        verbose_name='Name',
        max_length=256
    )
    owner = models.ForeignKey(
        to='users.User',
        related_name='collections',
        verbose_name='Owner',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    picture_big = models.ImageField(
        verbose_name='Big picture',
        upload_to='drop/picture_big',
        null=True,
        blank=True
    )
    picture_small = models.ImageField(
        verbose_name='Small picture',
        upload_to='drop/picture_small',
        null=True,
        blank=True
    )
    specifications = models.JSONField(
        verbose_name='Specifications',
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        verbose_name='Is active',
        default=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Collection'
        verbose_name_plural = 'Collections'

    def delete(self, *args, **kwargs):
        """
        Переопределение удаления модели
        """
        self.is_active = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SpecialCollection(models.Model):
    """
    Специальная коллекция (Модель)
    """
    name = models.CharField(
        verbose_name='Name',
        max_length=256
    )
    drops = models.ManyToManyField(
        to='drops.Drop',
        related_name='special_collection',
        verbose_name="Drop",
        through='drops.SpecialCollectionDrop'
    )

    class Meta:
        verbose_name = 'Special collection'
        verbose_name_plural = 'Special collections'

    def __str__(self):
        return self.name


class CollectionSubscription(models.Model):
    """
    Подписка на коллекцию (Модель)
    """
    user = models.ForeignKey(
        to='users.User',
        related_name="collection_subscription",
        verbose_name="User",
        on_delete=models.CASCADE
    )
    collection = models.ForeignKey(
        to='drops_collections.Collection',
        related_name="collection_subscription",
        verbose_name="Collection",
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(
        verbose_name='Is active',
        default=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Collection subscription'
        verbose_name_plural = 'Collections subscriptions'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'collection'],
                name='unique_collection_subscription'
            )
        ]


class CollectionLike(models.Model):
    """
    Лайк коллекции (Модель)
    """
    collection = models.ForeignKey(
        to='drops_collections.Collection',
        related_name='collection_like',
        verbose_name='Collection',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        to='users.User',
        related_name='collection_like',
        verbose_name='User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        verbose_name='Is active',
        default=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Collection Like'
        verbose_name_plural = 'Collections Likes'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'collection'],
                name='unique_collection_like'
            )
        ]

    def __str__(self):
        return f'{self.collection} {self.user}'


class CollectionView(models.Model):
    """
    Просмотр коллекции (Модель)
    """
    collection = models.ForeignKey(
        to='drops_collections.Collection',
        related_name='collection_view',
        verbose_name='Collection',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        to='users.User',
        related_name='collection_view',
        verbose_name='User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Collection view'
        verbose_name_plural = 'Collections views'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'collection'],
                name='unique_collection_view'
            )
        ]

    def __str__(self):
        return f'{self.collection} {self.user}'


