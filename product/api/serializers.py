from rest_framework import serializers
from ..models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    supplier = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    in_cart = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'code',
            'current_price', 'initial_price',
            'supplier',
            'image_url',
            'category',
            'in_cart'
        ]

    def get_image_url(self, obj):
        return 'https://picsum.photos/id/1047/100/100'

    def get_supplier(self, obj):
        return obj.supplier_id

    def get_category(self, obj):
        return obj.category_id

    def get_in_cart(self, obj):
        in_cart = self.context.get('ids_in_cart', dict())
        return in_cart.get(obj.id, 0)


class CategoryDictSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']
