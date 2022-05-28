
class Cart:
    def __init__(self, user=None):
        self.user = user

    def get_total_sum(self):
        from order.models import Order
        from product.price_utils import M
        total_sum = 0
        orders = Order.objects.filter(
            buyer=self.get_buyer(),
            status__is_cart=True
        )
        for order in orders:
            total_sum += order.order_sum

        return M(total_sum)

    def get_buyer(self):
        return self.user.get_buyer()

    def get_products_in_cart(self):
        from order.models import OrderItem

        items = OrderItem.objects.filter(order__status__is_cart=True)\
            .values_list('product', 'count')

        return dict(items)
