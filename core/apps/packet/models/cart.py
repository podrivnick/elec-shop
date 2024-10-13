from django.contrib.auth import get_user_model
from django.db import models

from core.apps.main.models.products import Products
from core.apps.packet.entities.cart import CartEntity


class CartQueryset(models.QuerySet):
    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Пользователь",
    )
    product = models.ForeignKey(
        to=Products,
        on_delete=models.CASCADE,
        verbose_name="Товар",
    )
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name="Количество")
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления",
    )

    class Meta:
        db_table = "cart"
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"

    # objects = CartQueryset().as_manager()

    def to_entity(self) -> CartEntity:
        return CartEntity(
            user=self.user,
            product=self.product,
            quantity=self.quantity,
            session_key=self.session_key,
            created_timestamp=self.created_timestamp,
        )

    # def products_price(self): noqa
    #     return round(self.product.sell_price() * self.quantity, 2)    noqa

    def __str__(self):
        if self.user:
            return f"Корзина {self.user.username} | Товар {self.product.name} | Количество {self.quantity}"

        return f"Анонимная корзина | Товар {self.product.name} | Количество {self.quantity}"
