from django.db import transaction

from .models import Order, OrderStatus, OrderItem


def get_or_create_cart(buyer, seller):
    with transaction.atomic():
        orders = Order.objects.filter(
            buyer=buyer,
            seller=seller,
            status__is_cart=True
        )
        carts_count = orders.count()
        if carts_count > 1:
            raise Exception(f'Found {carts_count} cart-orders for seller {seller.id} and buyer {buyer.id}')
        if carts_count == 0:
            status = OrderStatus.objects.filter(is_cart=True).first()
            if not status:
                raise Exception('No OrderStatus with "is_cart=True" found.')
            cart = Order.objects.create(
                buyer=buyer,
                seller=seller,
                status=status,
            )
            return cart
        return orders.first()


def get_cart_item(buyer, item_id):
    return OrderItem.objects.filter(
        order__buyer=buyer,
        order__status__is_cart=True,
        id=item_id
    ).first()


def get_cart(buyer, order_id):
    return Order.objects.filter(
        buyer=buyer,
        status__is_cart=True,
        id=order_id
    ).first()
