from rest_framework import views
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from utils.views import CustomApiView

from ..models import Order
from ..cart import get_or_create_cart, get_cart_item, get_cart
from . import serializers as cart_serializers


class CartView(CustomApiView):
    permission_classes = [IsAuthenticated]

    def get_product(self):
        from product.models import Product
        product = Product.objects.filter(id=self.request.data.get('product_id')).first()
        if not product or not product.supplier:
            raise NotFound
        return product

    def get_buyer(self):
        return self.request.user.get_buyer()

    def get_cart(self, supplier):
        return get_or_create_cart(
            buyer=self.get_buyer(),
            seller=supplier
        )


class GetCartListView(CustomApiView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        carts = Order.objects.filter(
            buyer=request.user.get_buyer(),
            status__is_cart=True
        )
        serializer = cart_serializers.CartListSerializer(carts, many=True)

        carts_data = serializer.data
        total_sum = 0
        for order in carts_data:
            total_sum += order.get('order_sum')

        return Response({
            'carts': carts_data,
            'sum': total_sum
        })


class GetCartDetailView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        carts = Order.objects.filter(
            buyer=request.user.get_buyer(),
            status__is_cart=True
        )
        order = carts.filter(id=request.GET.get('order_id')).first()

        if not order:
            raise NotFound
        serializer = cart_serializers.CartDetailSerializer(order)
        return Response(serializer.data)


class AddToCartView(CartView):
    def post(self, request):
        from order.cart_service import Cart
        product = self.get_product()
        cart = self.get_cart(product.supplier)

        cart_service = Cart(user=request.user)
        cart_item = cart.add_product(product, count=int(request.data.get('count', 0)))
        return Response({
            'id': cart_item.id if cart_item else None,
            'count': cart_item.count if cart_item else 0,
            'order_id': cart.id,
            'cart_sum': cart_service.get_total_sum()
        })


class RemoveFromCartView(CartView):
    def post(self, request):
        item = get_cart_item(buyer=self.get_buyer(), item_id=request.data.get('order_item_id'))
        if not item:
            raise NotFound
        item.delete()
        return Response({
            'result': 'ok',
        })


class ClearCartView(CartView):
    def post(self, request):
        cart = get_cart(buyer=self.get_buyer(), order_id=request.data.get('order_id'))
        if not cart:
            raise NotFound
        cart.delete()
        return Response({
            'result': 'ok',
        })
