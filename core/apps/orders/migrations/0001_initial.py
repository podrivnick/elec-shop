# Generated by Django 5.0.6 on 2024-10-05 17:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_receiver', models.CharField(max_length=50, null=True, verbose_name='Имя получателя')),
                ('surname_receiver', models.CharField(max_length=50, null=True, verbose_name='Фамилия получателя')),
                ('data_created_order', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')),
                ('phone_number', models.CharField(max_length=22, verbose_name='Номер телефона')),
                ('required_delivery', models.BooleanField(default=False, verbose_name='Требуется доставка')),
                ('delivery_address', models.CharField(max_length=100, verbose_name='Место доставки')),
                ('payment_on_get', models.BooleanField(default=False, verbose_name='Оплата при получении')),
                ('has_paid', models.BooleanField(default=False, verbose_name='Оплачено')),
                ('status', models.TextField(default='Обрабатывается', max_length=40, verbose_name='Статус заказа')),
                ('email', models.EmailField(blank=True, max_length=80, null=True, verbose_name='Почта')),
                ('total_price', models.DecimalField(decimal_places=3, default=0, max_digits=17, null=True, verbose_name='Общая стоимость')),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Название')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Цена')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Количество')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')),
                ('product', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='main.products', verbose_name='Продукт')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.orders', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Заказанный товар',
                'verbose_name_plural': 'Заказанные товары',
                'db_table': 'order_item',
            },
        ),
    ]
