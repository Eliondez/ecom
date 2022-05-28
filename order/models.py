from django.db import models, transaction
from django.core.validators import MinValueValidator

from product.price_utils import M


class OrderStatus(models.Model):
    value = models.SmallIntegerField(
        verbose_name='Значение',
    )
    name = models.CharField(
        max_length=64,
        verbose_name='Название статуса'
    )

    is_cart = models.BooleanField(
        verbose_name='Корзина',
        default=False,
    )

    is_draft = models.BooleanField(
        verbose_name='Черновик',
        default=False
    )

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    product = models.ForeignKey(
        'product.Product',
        verbose_name='Товар',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    count = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        default=1,
        verbose_name=''
    )
    price = models.DecimalField(
        validators=[MinValueValidator(0)],
        decimal_places=2,
        max_digits=16,
        verbose_name='Цена'
    )
    order = models.ForeignKey(
        'Order',
        verbose_name='Заказ',
        on_delete=models.CASCADE,
        related_name='items'
    )

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'

    def __str__(self):
        return self.product.name if self.product else '-- товар удалён --'

    @property
    def sum(self):
        return M(self.count * self.price)


class Order(models.Model):

    status = models.ForeignKey(
        'OrderStatus',
        on_delete=models.CASCADE,
        verbose_name='Покупатель'
    )
    buyer = models.ForeignKey(
        'counterparty.Counterparty',
        on_delete=models.SET_NULL,
        verbose_name='Покупатель',
        related_name='buy_orders',
        null=True,
        blank=True
    )
    seller = models.ForeignKey(
        'counterparty.Counterparty',
        on_delete=models.SET_NULL,
        verbose_name='Продавец',
        related_name='sell_orders',
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        'user.User',
        on_delete=models.SET_NULL,
        verbose_name='Пользователь',
        help_text='Тот, кто инициировал создание заказа. Обычно - покупатель',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ № {self.id}' if self.id else 'Новый заказ'

    def add_product(self, product, count=1):
        with transaction.atomic():
            item = self.items.filter(product=product).first()
            if count <= 0 and not item:
                return None
            if not item:
                item = OrderItem.objects.create(
                    order=self,
                    product=product,
                    count=count,
                    price=product.current_price
                )
            else:
                item.price = product.current_price
                item.count += count
                if item.count <= 0:
                    item.delete()
                    return None
                else:
                    item.save()
        return item

    def remove_item(self, product):
        self.items.filter(product=product).delete()

    @property
    def order_sum(self):
        res = 0
        for item in self.items.all():
            res += item.sum
        return res
