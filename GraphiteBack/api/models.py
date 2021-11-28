from datetime import datetime
from enum import unique

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class UserManager(BaseUserManager):
    """
    Менеджер пользователя (Модель)
    """
    use_in_migrations = True

    def _create_user(self, wallet_number, password, **extra_fields):
        """
        База создания пользователя
        """
        if not wallet_number:
            raise ValueError('The given email must be set')
        wallet_number = wallet_number
        user = self.model(wallet_number=wallet_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, wallet_number, password=None, **extra_fields):
        """
        Создание пользователя
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(wallet_number, password, **extra_fields)

    def create_superuser(self, wallet_number, password, **extra_fields):
        """
        Создание суперпользователя
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(wallet_number, password, **extra_fields)


class User(AbstractUser):
    """
    Пользователь (Модель)
    """

    class VerifyStatus(models.TextChoices):
        """
         Статус верификации
        """
        NOT_VERIFIED = 'not_verified', 'Not verified'
        MODERATION = 'moderation', 'Moderation'
        VERIFIED = 'verified', 'Verified'

    class ProfileType(models.TextChoices):
        """
         Тип профиля
        """
        ENTITY = 'entity', 'Entity'
        INDIVIDUAL = 'individual', 'Individual'

    username = None

    wallet_number = models.CharField('Wallet number', unique=True, max_length=20)
    owner_key = models.CharField('Owner key', max_length=256)

    avatar = models.ImageField('Avatar', upload_to='user/avatars', null=True, blank=True)
    cover = models.ImageField('Cover', upload_to='user/cover', null=True, blank=True)

    profile_type = models.CharField('Profile Type', max_length=20, choices=ProfileType.choices,
                                    default=ProfileType.INDIVIDUAL)
    verify_status = models.CharField('Verify Status', max_length=20, choices=VerifyStatus.choices,
                                     default=VerifyStatus.NOT_VERIFIED)

    drops = models.ManyToManyField('Drop', related_name='drops_owner', verbose_name="Drops", through='OwnerDrop')
    collections = models.ManyToManyField('Collection', related_name='user_collections', verbose_name='Collections',
                                         through='OwnerCollection')

    user_subscriptions = models.ManyToManyField('self', related_name='users_subscriptions', symmetrical=False,
                                                verbose_name="Users subscribers", through='UserUserSubscription')
    drop_subscriptions = models.ManyToManyField('Drop', related_name='drops_subscriptions',
                                                verbose_name="Drops subscribers", through='UserDropSubscription')
    collections_subscriptions = models.ManyToManyField('Collection', related_name='collections_subscriptions',
                                                       verbose_name="Collections subscribers",
                                                       through='UserCollectionSubscription')

    is_verify = models.BooleanField("Verify", default=False)
    email_notification = models.BooleanField('email-notification', default=False)

    description = models.TextField("Description", null=True, blank=True)

    instagram = models.CharField('Instagram', max_length=50, null=True, blank=True)
    twitter = models.CharField('Twitter', max_length=50, null=True, blank=True)
    discord = models.CharField('Discord', max_length=50, null=True, blank=True)
    tiktok = models.CharField('Tiktok', max_length=50, null=True, blank=True)
    telegram = models.CharField('Telegram', max_length=50, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'wallet_number'
    REQUIRED_FIELDS = ['owner_key']

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.wallet_number} {self.last_name} {self.first_name}"


class PassportData(models.Model):
    user = models.OneToOneField(User, verbose_name='Password data', related_name='user_passport',
                                on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField('First name', max_length=50)
    last_name = models.CharField('Last name', max_length=50)
    birthday = models.DateField('Birthday')
    passport_series = models.CharField('Passport series', max_length=50)
    passport_number = models.IntegerField('Passport number')
    passport_issue_date = models.DateField('Passport issue date')
    passport_expiration_date = models.DateField('Passport Expiration Date')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Categories(models.Model):
    name = models.CharField(max_length=256, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.name}'


class Tags(models.Model):
    name = models.CharField(max_length=256, unique=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return f'{self.name}'


class Drop(models.Model):
    class BlockchainType(models.TextChoices):
        """
         Статус верификации
        """
        WAX = 'wax', 'WAX'
        ANCHOR = 'anchor', 'Anchor'

    class SellType(models.TextChoices):
        """
         Статус верификации
        """
        AUCTION = 'auction', 'Auction'
        SELL = 'sell', 'Sell'

    blockchain_type = models.CharField('Blockchain type', max_length=20, choices=BlockchainType.choices,
                                       null=True, blank=True)
    blockchain_address = models.CharField('Blockchain address', max_length=256, blank=True,
                                          null=True)
    blockchain_identifier = models.CharField('Blockchain identifier', max_length=256, blank=True,
                                             null=True)

    name = models.CharField('Name', max_length=256)
    descriptions = models.TextField('Description', null=True, blank=True)

    category = models.ForeignKey(
        Categories, related_name='drops', verbose_name='Category',
        on_delete=models.SET_NULL, null=True, blank=True
    )

    tags = models.ManyToManyField(Tags, related_name='drops', verbose_name='Tags', blank=True)

    artists = models.ForeignKey(
        User, related_name='drop_artist', verbose_name='Artist',
        on_delete=models.SET_NULL, null=True, blank=True,
    )

    sell_type = models.CharField('Sell type', max_length=20, choices=SellType.choices,
                                 null=True, blank=True)
    sell_count = models.IntegerField('Sell count', default=0)
    all_sell_count = models.IntegerField('All sell count', default=0)
    init_cost = models.FloatField('Init cost', default=0)
    min_rate = models.FloatField('Min rate', default=0)

    picture_big = models.ImageField('Big picture', upload_to='drop/picture_big', null=True, blank=True)
    picture_small = models.ImageField('Small picture', upload_to='drop/picture_small', null=True, blank=True)
    to_sell = models.BooleanField('To sell', default=False)
    url_landing = models.CharField('Landing URL', max_length=256, null=True, blank=True)

    auction_deadline = models.DateTimeField('Auction deadline', null=True, blank=True)
    royalty = models.FloatField('Royalty', default=0,
                                validators=[
                                    MaxValueValidator(100),
                                    MinValueValidator(0)
                                ])

    parent = models.ForeignKey(
        'self', related_name='parent_drop', verbose_name='Parent',
        on_delete=models.SET_NULL, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Обработка полей перед сохранением модели
        """

        if not self.auction_deadline:
            self.auction_deadline = None
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Drop'
        verbose_name_plural = 'Drops'

    def __str__(self):
        return self.name


class Collection(models.Model):
    name = models.CharField('Name', max_length=256)
    drops = models.ManyToManyField(Drop, related_name='collection', verbose_name='Drops', through='CollectionDrop')
    specifications = models.JSONField('Specifications', null=True,blank=True)

    class Meta:
        verbose_name = 'Collection'
        verbose_name_plural = 'Collections'

    def __str__(self):
        return self.name


class DropLike(models.Model):
    drop = models.ForeignKey(
        Drop, related_name='drop_likes', verbose_name='Drop',
        on_delete=models.CASCADE, null=True, blank=True
    )
    user = models.ForeignKey(
        User, related_name='drop_likes', verbose_name='User',
        on_delete=models.SET_NULL, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Drop Like'
        verbose_name_plural = 'Drop Likes'
        constraints = [
            models.UniqueConstraint(fields=['user', 'drop'], name='unique_user_drop_like')
        ]

    def __str__(self):
        return f'{self.drop} {self.user}'


class CollectionLike(models.Model):
    collection = models.ForeignKey(
        Collection, related_name='collection_likes', verbose_name='Collection',
        on_delete=models.CASCADE, null=True, blank=True
    )
    user = models.ForeignKey(
        User, related_name='collection_likes', verbose_name='User',
        on_delete=models.SET_NULL, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Collection Like'
        verbose_name_plural = 'Collections Likes'
        constraints = [
            models.UniqueConstraint(fields=['user', 'collection'], name='unique_user_collections_like')
        ]

    def __str__(self):
        return f'{self.collection} {self.user}'


class DropView(models.Model):
    drop = models.ForeignKey(
        Drop, related_name='drop_views', verbose_name='Drop',
        on_delete=models.CASCADE, null=True, blank=True
    )
    user = models.ForeignKey(
        User, related_name='drop_views', verbose_name='User',
        on_delete=models.SET_NULL, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'View'
        verbose_name_plural = 'Views'
        constraints = [
            models.UniqueConstraint(fields=['user', 'drop'], name='unique_user_drop_views')
        ]

    def __str__(self):
        return f'{self.drop} {self.user}'


class CollectionView(models.Model):
    collection = models.ForeignKey(
        Collection, related_name='collection_views', verbose_name='Collection',
        on_delete=models.CASCADE, null=True, blank=True
    )
    user = models.ForeignKey(
        User, related_name='collection_views', verbose_name='User',
        on_delete=models.SET_NULL, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'View'
        verbose_name_plural = 'Views'
        constraints = [
            models.UniqueConstraint(fields=['user', 'collection'], name='unique_user_collection_views')
        ]

    def __str__(self):
        return f'{self.collection} {self.user}'


class CollectionDrop(models.Model):
    drop_collection = models.ForeignKey(Collection, related_name='collection_drop', verbose_name="Drop collection",
                                        on_delete=models.CASCADE)
    drop = models.ForeignKey(Drop, related_name='collection_drop', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Collection drop'
        verbose_name_plural = 'Collections Drops'
        constraints = [
            models.UniqueConstraint(fields=['drop_collection', 'drop'], name='unique_collection_drop')
        ]


class OwnerDrop(models.Model):
    drop_owner = models.ForeignKey(User, related_name='owner_drop', verbose_name="Drop owner", on_delete=models.CASCADE)
    drop = models.ForeignKey(Drop, related_name='drop', verbose_name="Drop", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User drop'
        verbose_name_plural = 'Users Drops'
        constraints = [
            models.UniqueConstraint(fields=['drop_owner', 'drop'], name='unique_user_drop')
        ]


class OwnerCollection(models.Model):
    collection_owner = models.ForeignKey(User, related_name='collection_ovner', verbose_name="Clloection owner",
                                         on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, verbose_name="collection", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User collections'
        verbose_name_plural = 'Users collections'
        constraints = [
            models.UniqueConstraint(fields=['collection_owner', 'collection'], name='unique_owner_collection')
        ]


class UserUserSubscription(models.Model):
    current_user = models.ForeignKey(User, related_name="current_user", verbose_name="User", on_delete=models.CASCADE)
    user_of_interest = models.ForeignKey(User, related_name="user_of_interest", verbose_name="User of interest",
                                         on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User user subscription'
        verbose_name_plural = 'Users user subscriptions'
        constraints = [
            models.UniqueConstraint(fields=['current_user', 'user_of_interest'], name='unique_user_subscriber')
        ]


class UserDropSubscription(models.Model):
    subscriber = models.ForeignKey(User, verbose_name="Subscriber", on_delete=models.CASCADE)
    drop = models.ForeignKey(Drop, verbose_name="drop", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User drop subscription'
        verbose_name_plural = 'Users drops subscriptions'
        constraints = [
            models.UniqueConstraint(fields=['subscriber', 'drop'], name='unique_drop_subscriber')
        ]


class UserCollectionSubscription(models.Model):
    subscriber = models.ForeignKey(User, verbose_name="Subscriber", on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, verbose_name="collection", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User collection subscription'
        verbose_name_plural = 'Users collection subscriptions'
        constraints = [
            models.UniqueConstraint(fields=['subscriber', 'collection'], name='unique_collection_subscriber')
        ]
