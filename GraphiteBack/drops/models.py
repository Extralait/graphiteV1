import blank
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from model_utils import FieldTracker


class Category(models.Model):
    """
    Категория Дропа (Модель)
    """
    name = models.CharField(
        verbose_name='Name',
        max_length=256,
        unique=True,
        primary_key=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        """
        Обработка полей перед сохранением модели
        """
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class Tag(models.Model):
    """
    Тег Дропа (Модель)
    """
    name = models.CharField(
        verbose_name='Name',
        max_length=256,
        unique=True,
        primary_key=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def save(self, *args, **kwargs):
        """
        Обработка полей перед сохранением модели
        """
        self.name = self.name.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class Drop(models.Model):
    """
    Дроп (Модель)
    """

    class BlockchainType(models.TextChoices):
        """
        Тип blockchain
        """
        WAX = 'wax', 'WAX'
        ANCHOR = 'anchor', 'Anchor'

    class SellType(models.TextChoices):
        """
        Тип продажи
        """
        AUCTION = 'auction', 'Auction'
        SELL = 'sell', 'Sell'

    blockchain_type = models.CharField(
        verbose_name='Blockchain type',
        max_length=20,
        choices=BlockchainType.choices,
        null=True,
        blank=True
    )
    blockchain_address = models.CharField(
        verbose_name='Blockchain address',
        max_length=256,
        blank=True,
        null=True
    )
    blockchain_identifier = models.CharField(
        verbose_name='Blockchain identifier',
        max_length=256,
        blank=True,
        null=True
    )
    name = models.CharField(
        verbose_name='Name',
        max_length=256)
    descriptions = models.TextField(
        verbose_name='Description',
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        to='drops.Category',
        related_name='drop',
        verbose_name='Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    tags = models.ManyToManyField(
        'drops.Tag',
        related_name='drop',
        verbose_name='Tags',
        blank=True
    )
    artist = models.ForeignKey(
        to='users.User',
        related_name='artists_drops',
        verbose_name='Artist',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        to='users.User',
        related_name='owners_drops',
        verbose_name='Owner',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    sell_type = models.CharField(
        verbose_name='Sell type',
        max_length=20,
        choices=SellType.choices,
        null=True,
        blank=True
    )
    sell_count = models.IntegerField(
        verbose_name='Sell count',
        default=0,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0)
        ],
    )
    in_stock = models.IntegerField(
        verbose_name='In Stock',
        default=0,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0)
        ],
    )
    all_count = models.IntegerField(
        verbose_name='All count',
        validators=[
            MinValueValidator(0)
        ],
    )
    init_cost = models.FloatField(
        verbose_name='Init cost',
        default=0,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0)
        ],
    )
    min_rate = models.FloatField(
        verbose_name='Min rate',
        default=0,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0)
        ],
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
    to_sell = models.BooleanField(
        verbose_name='To sell',
        default=False,
        blank=True
    )
    url_landing = models.CharField(
        verbose_name='Landing URL',
        max_length=256,
        null=True,
        blank=True
    )
    auction_deadline = models.DateTimeField(
        verbose_name='Auction deadline',
        default=None,
        null=True,
        blank=True,
    )
    royalty = models.FloatField(
        verbose_name='Royalty',
        default=0,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ],
        null=True,
        blank=True
    )
    specifications = models.JSONField(
        verbose_name='Specifications',
        null=True,
        blank=True
    )
    from_collection = models.ForeignKey(
        to='drops_collections.Collection',
        related_name='drops',
        verbose_name='From collection',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    parent = models.ForeignKey(
        to='self',
        related_name='drop_parent',
        verbose_name='Parent',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        verbose_name='Is active',
        default=True,
    )
    level = models.IntegerField(
        verbose_name='Level',
        default=0,
        validators=[
            MinValueValidator(0)
        ],
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tracker = FieldTracker(fields=['to_sell', 'sell_type'])

    class Meta:
        verbose_name = 'Drop'
        verbose_name_plural = 'Drops'

    def save(self, *args, **kwargs):
        """
        Обработка полей перед сохранением модели
        """
        if not self.pk and not self.parent:
            self.in_stock = self.all_count
        if self.sell_count:
            if self.sell_count > self.in_stock:
                self.sell_count = self.in_stock
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Переопределение удаления модели
        """
        if self.in_stock:
            self.is_active = False
            super().save(*args, **kwargs)
        else:
            super().delete()

    def __str__(self):
        return self.name


class DropSubscription(models.Model):
    """
    Подписка на дроп (Модель)
    """
    user = models.ForeignKey(
        to='users.User',
        related_name="drop_subscription",
        verbose_name="User",
        on_delete=models.CASCADE
    )
    drop = models.ForeignKey(
        to='drops.Drop',
        related_name="drop_subscription",
        verbose_name="Drop",
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(
        verbose_name='Is active',
        default=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Drop subscription'
        verbose_name_plural = 'Drops subscriptions'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'drop'],
                name='unique_drop_subscription'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.drop}'


class DropLike(models.Model):
    """
    Лак дропа (Модель)
    """
    drop = models.ForeignKey(
        to='drops.Drop',
        related_name='drop_like',
        verbose_name='Drop',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        to='users.User',
        related_name='drop_like',
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
        verbose_name = 'Drop like'
        verbose_name_plural = 'Drop likes'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'drop'],
                name='unique_drop_like'
            )
        ]

    def __str__(self):
        return f'{self.drop} {self.user}'


class DropView(models.Model):
    """
    Просмотр дропа (Модель)
    """
    drop = models.ForeignKey(
        to='drops.Drop',
        related_name='drop_view',
        verbose_name='Drop',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        to='users.User',
        related_name='drop_view',
        verbose_name='User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Drop view'
        verbose_name_plural = 'Drops views'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'drop'],
                name='unique_drop_view'
            )
        ]

    def __str__(self):
        return f'{self.drop} {self.user}'


class SpecialCollectionDrop(models.Model):
    """
    Специальная коллекция (Модель)
    """
    collection = models.ForeignKey(
        to='drops_collections.SpecialCollection',
        related_name='special_collection_drop',
        verbose_name='Collection',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    drop = models.ForeignKey(
        to='drops.Drop',
        related_name='special_collection_drop',
        verbose_name='Drop',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    level = models.IntegerField(
        verbose_name='Level',
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )

    class Meta:
        verbose_name = 'Special collection drop'
        verbose_name_plural = 'Special collections drops'
        constraints = [
            models.UniqueConstraint(
                fields=['drop', 'collection'],
                name='unique_special_collection_drop'
            )
        ]

    def __str__(self):
        return f'{self.collection} {self.drop}'