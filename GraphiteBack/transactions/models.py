from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
class Transaction(models.Model):
    """
    Транзакция (Модель)
    """
    drop = models.ForeignKey(
        to='drops.Drop',
        related_name='drop_transactions',
        verbose_name='Drop',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    owner = models.ForeignKey(
        to='users.User',
        related_name='owner_transactions',
        verbose_name='Owner',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    buyer = models.ForeignKey(
        to='users.User',
        related_name='buyer_transactions',
        verbose_name='Buyer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    copies_count = models.IntegerField(
        verbose_name='Copies count',
        validators=[
            MinValueValidator(0)
        ],
        null=True,
        blank=True
    )
    unit_price = models.FloatField(
        verbose_name='Cost',
        default=0,
        null=True,
        blank=True
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
        default=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def save(self, *args, **kwargs):
        """
        Обработка полей перед сохранением модели
        """
        if not self.pk:
            self.owner = self.drop.owner
            if not self.drop.parent:
                self.royalty = 0
            else:
                self.royalty = self.drop.parent.royalty
            if not self.unit_price:
                self.unit_price = self.drop.init_cost
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Переопределение удаления модели
        """
        self.is_active = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.drop} {self.owner} {self.buyer}'