from datetime import datetime
from enum import unique

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
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


class ProfileType(models.Model):
    """
    Тип профиля
    """
    name = models.CharField("Name", unique=True, max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profile type'
        verbose_name_plural = 'Profile types'

    def __str__(self):
        return self.name


class VerifyStatus(models.Model):
    """
    Статус верификации
    """
    name = models.CharField("Name", unique=True, max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Verify status'
        verbose_name_plural = 'Verify statuses'

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Пользователь (Модель)
    """
    username = None

    wallet_number = models.CharField('Wallet number', unique=True, max_length=20)
    owner_key = models.CharField('Owner_key', max_length=256)

    avatar = models.ImageField('Avatar', upload_to='avatars', null=True, blank=True)
    cover = models.ImageField('Cover', upload_to='cover', null=True, blank=True)

    profile_type = models.ForeignKey(ProfileType, verbose_name="Profile Type", null=True, blank=True,
                                     on_delete=models.SET_NULL)
    verify_status = models.ForeignKey(VerifyStatus, verbose_name="Verify Status", null=True, blank=True,
                                      on_delete=models.SET_NULL)

    galleries = models.ManyToManyField('Gallery', related_name='user_galleries', verbose_name="Galleries",through='UserGallery')
    users_subscriptions = models.ManyToManyField('self', related_name='user_users_subscriptions',symmetrical=False, verbose_name="Users subscribers",through='UserUserSubscription')
    galleries_subscriptions = models.ManyToManyField('Gallery', related_name='user_galleries_subscriptions', verbose_name="Galleries subscribers",through='UserGallerySubscription')

    is_verify = models.BooleanField("Verify", default=False)
    email_notification = models.BooleanField('email-notification', default=False)

    description = models.TextField("Description", null=True, blank=True)

    instagram = models.CharField('Instagram', max_length=50, null=True, blank=True)
    twitter = models.CharField('Twitter', max_length=50, null=True, blank=True)
    discord = models.CharField('Discord', max_length=50, null=True, blank=True)
    tiktok = models.CharField('Tiktok', max_length=50, null=True, blank=True)
    telegram = models.CharField('Telegram', max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'wallet_number'
    REQUIRED_FIELDS = ['owner_key']

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.wallet_number} {self.last_name} {self.first_name}"


class Gallery(models.Model):
    name = models.CharField("Name", unique=True, max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'

    def __str__(self):
        return self.name


class UserGallery(models.Model):
    owner = models.ForeignKey(User, verbose_name="Owner", on_delete=models.CASCADE)
    gallery = models.ForeignKey(Gallery, verbose_name="Gallery", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User gallery'
        verbose_name_plural = 'Users galleries'


class UserUserSubscription(models.Model):
    current_user = models.ForeignKey(User, related_name="current_user",verbose_name="User", on_delete=models.CASCADE)
    user_of_interest = models.ForeignKey(User, related_name="user_of_interest",verbose_name="User of interest", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User user subscription'
        verbose_name_plural = 'Users user subscriptions'


class UserGallerySubscription(models.Model):
    subscriber = models.ForeignKey(User, verbose_name="Subscriber", on_delete=models.CASCADE)
    gallery = models.ForeignKey(Gallery, verbose_name="Gallery", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User gallery subscription'
        verbose_name_plural = 'Users galleries subscriptions'

