from django.contrib import admin
from .models import Product, Category, Currency


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'is_active',
                    'current_price',
                    'currency_price', 'base_currency_price')


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'sign', 'rate')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Currency, CurrencyAdmin)
