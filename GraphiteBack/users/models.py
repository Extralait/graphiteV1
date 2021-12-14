from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.safestring import mark_safe


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

    # Базовая информация о профиле
    wallet_number = models.CharField(
        verbose_name='Wallet number',
        unique=True,
        max_length=20
    )
    owner_key = models.CharField(
        verbose_name='Owner key',
        max_length=256
    )
    inn = models.CharField(
        verbose_name='INN',
        max_length=256,
        null=True,
        blank=True
    )
    balance = models.FloatField(
        verbose_name='Balance',
        default=0,
        validators=[
            MinValueValidator(0)
        ],
        null=True,
        blank=True
    )
    avatar = models.ImageField(
        verbose_name='Avatar',
        upload_to='user/avatars',
        null=True,
        blank=True
    )
    cover = models.ImageField(
        verbose_name='Cover',
        upload_to='user/cover',
        null=True,
        blank=True
    )
    profile_type = models.CharField(
        verbose_name='Profile type',
        max_length=20,
        choices=ProfileType.choices,
        null=True,
        blank=True
    )
    verify_status = models.CharField(
        verbose_name='Verify status',
        max_length=20,
        choices=VerifyStatus.choices,
        default=VerifyStatus.NOT_VERIFIED
    )
    email_notification = models.BooleanField(
        verbose_name='E-mail notification',
        default=False
    )
    description = models.CharField(
        verbose_name="Description",
        max_length=2000,
        null=True,
        blank=True
    )

    # Социальные сети
    instagram = models.CharField(
        verbose_name='Instagram',
        max_length=50,
        null=True,
        blank=True
    )
    twitter = models.CharField(
        verbose_name='Twitter',
        max_length=50,
        null=True,
        blank=True
    )
    discord = models.CharField(
        verbose_name='Discord',
        max_length=50,
        null=True,
        blank=True
    )
    tiktok = models.CharField(
        verbose_name='Tiktok',
        max_length=50,
        null=True,
        blank=True
    )
    telegram = models.CharField(
        verbose_name='Telegram',
        max_length=50,
        null=True,
        blank=True
    )
    website = models.CharField(
        verbose_name='Website',
        max_length=256,
        null=True,
        blank=True
    )

    # Подписки
    user_subscriptions = models.ManyToManyField(
        to='self',
        related_name='subscribers',
        symmetrical=False,
        verbose_name="Users subscribers",
        through='users.UserSubscription'
    )
    drop_subscriptions = models.ManyToManyField(
        to='drops.Drop',
        related_name='subscribers',
        verbose_name="Drops subscribers",
        through='drops.DropSubscription'
    )
    collection_subscriptions = models.ManyToManyField(
        to='drops_collections.Collection',
        related_name='subscribers',
        verbose_name="Collections subscribers",
        through='drops_collections.CollectionSubscription'
    )

    # Лайки
    drop_likes = models.ManyToManyField(
        to='drops.Drop',
        related_name='likes',
        verbose_name="Drops likes",
        through='drops.DropLike'
    )
    collections_likes = models.ManyToManyField(
        to='drops_collections.Collection',
        related_name='likes',
        verbose_name="Collections likes",
        through='drops_collections.CollectionLike'
    )

    # Просмотры
    user_views = models.ManyToManyField(
        to='users.User',
        related_name='views',
        symmetrical=False,
        verbose_name="Users views",
        through='users.UserView'
    )
    drop_views = models.ManyToManyField(
        to='drops.Drop',
        related_name='views',
        verbose_name="Drops views",
        through='drops.DropView'
    )
    collections_views = models.ManyToManyField(
        to='drops_collections.Collection',
        related_name='views',
        verbose_name="Collections views",
        through='drops_collections.CollectionView'
    )

    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'wallet_number'
    REQUIRED_FIELDS = ['owner_key']

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def avatar_tag(self):
        return mark_safe('<img src="/media/%s" width="150" height="94" />' % self.avatar)

    def cover_tag(self):
        return mark_safe('<img src="/media/%s" width="150" height="94" />' % self.cover)

    avatar_tag.short_description = 'Avatar'
    cover_tag.short_description = 'Cover'

    def delete(self, *args, **kwargs):
        """
        Переопределение удаления модели
        """
        self.is_active = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.wallet_number} {self.last_name} {self.first_name}"


class UsersGroup(models.Model):
    """
    Группы пользователей (Модель)
    """
    name = models.CharField(
        verbose_name='Name',
        max_length=256
    )
    users = models.ManyToManyField(
        to='users.User',
        related_name='users_groups',
        verbose_name="User",
        through='users.UsersGroupUser'
    )

    class Meta:
        verbose_name = 'User group'
        verbose_name_plural = 'Users groups'

    def __str__(self):
        return self.name


class UsersGroupUser(models.Model):
    """
    Пользователь в группе пользователей (Модель)
    """
    user_group = models.ForeignKey(
        to='users.UsersGroup',
        related_name='user_group_user',
        verbose_name='User group',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        to='users.User',
        related_name='user_group_user',
        verbose_name='User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
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

    class Meta:
        verbose_name = 'Users group user'
        verbose_name_plural = 'Users groups users'
        constraints = [
            models.UniqueConstraint(
                fields=['user_group', 'user'],
                name='unique_user_group_user'
            )
        ]

    def __str__(self):
        return f'{self.user_group} {self.user}'


class PassportData(models.Model):
    """
    Паспортные данные (Модель)
    """

    class VerifyStatus(models.TextChoices):
        """
        Статус верификации
        """
        NOT_VERIFIED = 'not_verified', 'Not verified'
        MODERATION = 'moderation', 'Moderation'
        VERIFIED = 'verified', 'Verified'

    user = models.OneToOneField(
        to='users.User',
        verbose_name='Passport data',
        related_name='passport_data',
        on_delete=models.CASCADE,
        primary_key=True
    )
    first_name = models.CharField(
        verbose_name='First name',
        max_length=50,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Last name',
        max_length=50,
        null=True,
        blank=True
    )
    birthday = models.DateField(
        verbose_name='Birthday',
        null=True,
        blank=True
    )
    passport_series = models.CharField(
        verbose_name='Passport series',
        max_length=50,
        null=True,
        blank=True
    )
    passport_number = models.IntegerField(
        verbose_name='Passport number',
        null=True,
        blank=True
    )
    passport_issue_date = models.DateField(
        verbose_name='Passport issue date',
        null=True,
        blank=True
    )
    passport_expiration_date = models.DateField(
        verbose_name='Passport Expiration Date',
        null=True,
        blank=True
    )
    verify_status = models.CharField(
        verbose_name='Verify Status',
        max_length=20,
        choices=VerifyStatus.choices,
        default=VerifyStatus.NOT_VERIFIED
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class UserSubscription(models.Model):
    """
    Подписка на пользователея (Модель)
    """
    subscriber = models.ForeignKey(
        to='users.User',
        related_name="user_subscriber",
        verbose_name="Subscriber",
        on_delete=models.CASCADE
    )
    subscription = models.ForeignKey(
        to='users.User',
        related_name="user_subscription",
        verbose_name="Subscription",
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(
        verbose_name='Is active',
        default=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User subscription'
        verbose_name_plural = 'Users subscriptions'
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'subscription'],
                name='unique_user_subscription'
            )
        ]


class UserView(models.Model):
    """
    Просмотр пользователя (Модель)
    """
    looking = models.ForeignKey(
        to='users.User',
        related_name="user_looking",
        verbose_name="Looking",
        on_delete=models.CASCADE
    )
    overlooked = models.ForeignKey(
        to='users.User',
        related_name="user_overlooked",
        verbose_name="Overlooked",
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User view'
        verbose_name_plural = 'Users views'
        constraints = [
            models.UniqueConstraint(
                fields=['looking', 'overlooked'],
                name='unique_user_view'
            )
        ]
