from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    current_counterparty = models.ForeignKey(
        'counterparty.Counterparty',
        blank=True,
        null=True,
        verbose_name='Контрагент',
        on_delete=models.SET_NULL
    )

    def get_buyer(self):
        cc = self.current_counterparty
        if not cc:
            return None
        if not cc.can_buy:
            return None
        return cc
