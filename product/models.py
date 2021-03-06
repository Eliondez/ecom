from django.db import models
from django.core.validators import MinValueValidator

from mptt.models import MPTTModel, TreeForeignKey


class Currency(models.Model):
    code = models.CharField(primary_key=True, verbose_name='Название', max_length=3)
    sign = models.CharField(verbose_name='Знак', max_length=3, blank=True)
    rate = models.DecimalField(verbose_name='Курс обмена', max_digits=16, decimal_places=8, default=1)

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'


class Category(MPTTModel):
    """
    python manage.py dumpdata product.Category > categories.json
    python manage.py loaddata categories.json
    """

    name = models.CharField(
        unique=True,
        max_length=256,
        verbose_name='Название'
    )
    parent = TreeForeignKey(
        'self',
        verbose_name='Родительская категория',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='children'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Показывать'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=512,
        verbose_name='Название'
    )
    code = models.CharField(
        max_length=128,
        verbose_name='Артикул'
    )
    supplier = models.ForeignKey(
        'counterparty.Counterparty',
        null=True,
        blank=True,
        verbose_name='Поставщик',
        on_delete=models.SET_NULL
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        verbose_name='Категория товара',
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        verbose_name='Активен',
        default=True
    )
    current_price = models.DecimalField(
        validators=[MinValueValidator(0)],
        decimal_places=2,
        max_digits=16,
        verbose_name='Текущая цена'
    )
    initial_price = models.DecimalField(
        validators=[MinValueValidator(0)],
        decimal_places=2,
        max_digits=16,
        null=True,
        blank=True,
        verbose_name='Изначальная цена',
        help_text='Если указана, товар будет показан "со скидкой"'
    )
    description = models.TextField(
        verbose_name='Описание товара',
        null=True,
        blank=True
    )
    image = models.ImageField(
        upload_to='product',
        null=True,
        blank=True,
        verbose_name='Картинка'
    )
    currency = models.ForeignKey(
        'Currency',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Валюта'
    )
    currency_price = models.DecimalField(
        verbose_name='Цена',
        decimal_places=2,
        max_digits=9,
        validators=[MinValueValidator(0)],
        default=0
    )
    base_currency_price = models.DecimalField(
        verbose_name='Цена в базовой валюте портала',
        decimal_places=2,
        max_digits=9,
        validators=[MinValueValidator(0)],
        default=0
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_currency(self):
        if not self.currency:
            self.currency = Currency.objects.get(code='EUR')
            self.save()
        return self.currency
