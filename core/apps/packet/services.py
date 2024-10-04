from django.db.models import Sum

from core.apps.main.models.products import Products

from .models import Cart


class AddToPacketProduct:
    def __init__(self, is_authenticated: bool, product_id, user_or_session_key):
        self.is_authenticated = is_authenticated
        self.product_id = product_id
        self.user_or_session_key = user_or_session_key

    def add_product_packet(self):
        product = Products.objects.get(id_product=self.product_id)

        # Определяем фильтр на основе аутентификации пользователя
        filter_kwargs = (
            {"user": self.user_or_session_key}
            if self.is_authenticated
            else {"session_key": self.user_or_session_key}
        )

        # Ищем пакет в корзине
        packet = Cart.objects.filter(product=product, **filter_kwargs).first()

        # Обновляем или создаем пакет
        if packet:
            packet.quantity += 1
            packet.save()
        else:
            Cart.objects.create(
                product=product,
                quantity=1,
                **filter_kwargs,
            )

        return packet


class DeleteCartFromPacketLogic:
    def __init__(self, cart_id):
        self.cart_id = cart_id

    def delete_cart_packet(self):
        cart = Cart.objects.get(pk=self.cart_id)
        cart.delete()


class ChangeCartQuantity:
    def __init__(
        self,
        is_authenticated: bool,
        user_or_session_key,
        is_plus: bool,
        cart_id,
    ):
        self.is_authenticated = is_authenticated
        self.user_or_session_key = user_or_session_key
        self.is_plus = is_plus
        self.cart_id = cart_id

    def change_cart_quantity(self):
        user_filter = (
            {"user": self.user_or_session_key}
            if self.is_authenticated
            else {"session_key": self.user_or_session_key}
        )

        cart = Cart.objects.filter(pk=self.cart_id).first()

        if not cart:
            return 0  # Обработакта отсутствия корзины

        if self.is_plus == "false":
            new_quantity = cart.quantity - 1
            if new_quantity <= 0:
                cart.delete()
            else:
                Cart.objects.filter(pk=self.cart_id).update(quantity=new_quantity)
        else:
            new_quantity = cart.quantity + 1
            Cart.objects.filter(pk=self.cart_id).update(quantity=new_quantity)

        carts_left = Cart.objects.filter(**user_filter).order_by("-quantity")

        total_quantity = carts_left.aggregate(Sum("quantity"))["quantity__sum"] or 0

        return carts_left, total_quantity
