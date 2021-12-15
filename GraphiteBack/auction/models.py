from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models



class Auction(models.Model):
    """
    Аукцион (Модель)
    """
    drop = models.ForeignKey(
        to='drops.Drop',
        verbose_name='Drop',
        related_name='auction',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    init_cost = models.FloatField(
        verbose_name='Init cost',
    )
    current_cost = models.FloatField(
        verbose_name='Init cost',
    )
    current_user = models.ForeignKey(
        to='users.User',
        verbose_name='Current user',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='auction_current_user'
    )
    min_rate = models.FloatField(
        verbose_name='Min rate',
    )
    sell_count = models.IntegerField(
        verbose_name='Sell count',
        validators=[
            MinValueValidator(0)
        ],
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
    is_active = models.BooleanField(
        verbose_name='Is active',
        default=True,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Auction'
        verbose_name_plural = 'Auctions'

    def save(self, *args, **kwargs):
        """
        Обработка полей перед сохранением
        """
        if not self.pk:
            self.init_cost = self.drop.init_cost
            self.current_cost = self.init_cost
            self.min_rate = self.drop.min_rate
            self.sell_count = self.drop.sell_count
            self.auction_deadline = self.drop.auction_deadline
            self.royalty = self.drop.royalty

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Переопределение удаления модели
        """
        if self.current_user:
            pass
        else:
            super().delete()

    def __str__(self):
        return self.drop


class AuctionUserBid(models.Model):
    """
    Ставка пользователя на аукцион (Модель)
    """
    user = models.ForeignKey(
        to='users.User',
        verbose_name='User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='auction_user_bid'
    )
    auction = models.ForeignKey(
        to='auction.Auction',
        verbose_name='Auction',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='auction_user_bid'
    )
    bid = models.FloatField(
        verbose_name='Bid',
        validators=[
            MinValueValidator(0)
        ],
    )
    is_active = models.BooleanField(
        verbose_name='Is active',
        default=True,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Auction user bid'
        verbose_name_plural = 'Auction users bids'

    def __str__(self):
        return f'{self.user} {self.auction}'


