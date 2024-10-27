from django.contrib.auth import get_user_model
from django.db import models

from core.apps.main.models.products import Products


class Orders(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_DEFAULT,
        null=True,
        verbose_name="Пользователь",
        blank=True,
        default=None,
    )
    name_receiver = models.CharField(
        max_length=50,
        verbose_name="Имя получателя",
        null=True,
    )
    surname_receiver = models.CharField(
        max_length=50,
        verbose_name="Фамилия получателя",
        null=True,
    )
    data_created_order = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания заказа",
    )
    phone_number = models.CharField(max_length=22, verbose_name="Номер телефона")
    required_delivery = models.BooleanField(
        default=False,
        verbose_name="Требуется доставка",
    )
    delivery_address = models.CharField(max_length=100, verbose_name="Место доставки")
    payment_on_get = models.BooleanField(
        default=False,
        verbose_name="Оплата при получении",
    )
    has_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    status = models.TextField(
        max_length=40,
        default="Обрабатывается",
        verbose_name="Статус заказа",
    )
    email = models.EmailField(
        max_length=80,
        blank=True,
        verbose_name="Почта",
        null=True,
    )
    total_price = models.DecimalField(
        max_digits=17,
        decimal_places=3,
        default=0,
        null=True,
        verbose_name="Общая стоимость",
    )

    class Meta:
        db_table = "order"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ № {self.pk} | Покупатель {self.user.first_name} {self.user.last_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(to=Orders, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(
        to=Products,
        on_delete=models.SET_DEFAULT,
        null=True,
        verbose_name="Продукт",
        default=None,
    )
    name = models.CharField(max_length=150, verbose_name="Название")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    created_timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата заказа",
    )

    class Meta:
        db_table = "order_item"
        verbose_name = "Заказанный товар"
        verbose_name_plural = "Заказанные товары"

    def __str__(self):
        return f"Товар {self.name} | Заказ № {self.order.pk}"
