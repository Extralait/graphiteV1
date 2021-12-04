from django.core.validators import MinValueValidator
from django.db import models


class Offer(models.Model):
    """
    Офер (Модель)
    """
    drop = models.ForeignKey(
        to='drops.Drop',
        related_name='drop_offer',
        verbose_name='Drop',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    owner = models.ForeignKey(
        to='users.User',
        related_name='owner_offer',
        verbose_name='Owner',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    buyer = models.ForeignKey(
        to='users.User',
        related_name='buyer_offer',
        verbose_name='Buyer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    unit_price = models.FloatField(
        verbose_name='Unit price',
        validators=[
            MinValueValidator(0)
        ],
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
    is_active = models.BooleanField(
        verbose_name='Is active',
        default=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Offer'
        verbose_name_plural = 'Offers'

    def save(self, *args, **kwargs):
        """
        Обработка полей перед сохранением модели
        """
        if not self.pk:
            self.owner = self.drop.owner
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Переопределение удаления модели
        """
        self.is_active = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.drop} {self.owner} {self.buyer}'