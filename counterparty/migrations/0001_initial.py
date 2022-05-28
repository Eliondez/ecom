# Generated by Django 4.0.3 on 2022-05-01 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Counterparty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Контрагент')),
                ('can_buy', models.BooleanField(default=True, verbose_name='Может покупать')),
                ('can_sell', models.BooleanField(default=True, verbose_name='Может продавать')),
            ],
            options={
                'verbose_name': '',
                'verbose_name_plural': '',
            },
        ),
    ]
