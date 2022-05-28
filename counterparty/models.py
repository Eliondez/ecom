from django.db import models


class Counterparty(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Контрагент',
        unique=True
    )

    can_buy = models.BooleanField(
        default=True,
        verbose_name='Может покупать'
    )

    can_sell = models.BooleanField(
        default=True,
        verbose_name='Может продавать'
    )

    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'

    def __str__(self):
        return self.name
