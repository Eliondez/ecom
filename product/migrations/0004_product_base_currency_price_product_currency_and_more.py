# Generated by Django 4.0.3 on 2022-05-30 16:54

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_currency_alter_product_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='base_currency_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена в базовой валюте портала'),
        ),
        migrations.AddField(
            model_name='product',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.currency', verbose_name='Валюта'),
        ),
        migrations.AddField(
            model_name='product',
            name='currency_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена'),
        ),
    ]
