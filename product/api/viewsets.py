from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from ..models import Product, Category
from product.api import serializers as product_serializers

from counterparty.models import Counterparty
from counterparty.api import serializers as counterparty_serializers

from ..price_utils import M


# todo: Вынести в отдельный файл
class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 40


class ProductViewset(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []

    queryset = Product.objects.all()
    serializer_class = product_serializers.ProductSerializer
    pagination_class = CustomPageNumberPagination

    available_dicts = {'categories', 'suppliers'}

    def parse_required_dicts(self):
        dicts_string = self.request.query_params.get('dicts', '')
        if dicts_string:
            dicts = set(dicts_string.split(','))
        else:
            dicts = set()
        return self.available_dicts & dicts

    def set_dicts(self, response, params):
        from counterparty.models import Counterparty

        needed_dicts = self.parse_required_dicts()

        response.data['dicts'] = {
            'available': self.available_dicts,
            'use_sample': '?dicts={}'.format(','.join(self.available_dicts))
        }

        param_map = {
            'categories': {
                'model': Category,
                'serializer': product_serializers.CategoryDictSerializer
            },
            'suppliers': {
                'model': Counterparty,
                'serializer': counterparty_serializers.CounterpartySerializer
            },
        }

        for param in params:
            name = param.get('name')
            if name not in needed_dicts:
                continue
            param_data = param_map[name]
            items = param_data.get('model').objects.filter(id__in=param.get('ids'))
            serializer_class = param_data.get('serializer')
            response.data['dicts'][name] = serializer_class(items, many=True).data

    def list(self, request, *args, **kwargs):
        from order.cart_service import Cart

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            ids_in_cart = Cart(user=request.user).get_products_in_cart()

            serializer = self.get_serializer(page,
                                             many=True,
                                             context={'ids_in_cart': ids_in_cart}
                                             )
            categories_set = set()
            suppliers_set = set()
            for item in page:
                categories_set.add(item.category_id)
                suppliers_set.add(item.supplier_id)
            res = self.get_paginated_response(serializer.data)
            self.set_dicts(res, [
                {'name': 'categories', 'ids': categories_set, 'model': Category},
                {'name': 'suppliers', 'ids': suppliers_set, 'model': Counterparty},
            ])
            return res

        serializer = self.get_serializer(queryset, many=True)
        res = serializer.data
        return Response(res)

    @action(detail=False, methods=['GET'])
    def create_test_products(self, request):
        from random import choice, randint, random
        from counterparty.models import Counterparty
        categories = list(Category.objects.all())
        suppliers = list(Counterparty.objects.all())

        products = []
        for i in range(100):
            price = M(randint(1, 100) + float(randint(0, 99)) / 100)
            if random() > 0.8:
                initial_price = price + M(float(randint(0, 99)) / 100)
            else:
                initial_price = None
            products.append(
                Product(
                    name=f'{randint(1000, 9999)}_товар_{i}',
                    code=f'{randint(1000, 9999)}-{randint(1000, 9999)}',
                    category=choice(categories),
                    supplier=choice(suppliers),
                    current_price=price,
                    initial_price=initial_price
                )
            )
        Product.objects.bulk_create(products)
        return Response({'status': 'password set'})
