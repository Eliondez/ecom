from rest_framework import serializers
from ..models import Order, OrderStatus, OrderItem

from counterparty.api import serializers as counterparty_serializers


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'count', 'price', 'sum'
        ]

    def get_count(self, obj):
        return int(obj.count)

    def get_product(self, obj):

        return {
            'id': obj.product.id,
            'name': obj.product.name,
            'code': obj.product.code,
        }


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = [
            'id', 'name'
        ]


class CartListSerializer(serializers.ModelSerializer):
    seller = counterparty_serializers.CounterpartySerializer()
    buyer = counterparty_serializers.CounterpartySerializer()
    order_items_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'buyer',
            'seller', 'order_sum',
            'order_items_count'
        ]

    def get_order_items_count(self, obj):
        return obj.items.count()


class CartDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    seller = counterparty_serializers.CounterpartySerializer()
    buyer = counterparty_serializers.CounterpartySerializer()

    class Meta:
        model = Order
        fields = [
            'id', 'buyer',
            'seller', 'user',
            'items', 'order_sum'
        ]
