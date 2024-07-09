from .models import Cart
from main_favorite.models import Products


class AddToPacketProduct:

    def __init__(self, is_authenticate: bool, product_id, user_or_session_key):
        self.is_authenticate = is_authenticate
        self.product_id = product_id
        self.user_or_session_key = user_or_session_key

    def add_product_packet(self):
        product = Products.objects.get(id_product=self.product_id)

        # Определяем фильтр на основе аутентификации пользователя
        filter_kwargs = {'user': self.user_or_session_key} if self.is_authenticate else \
                        {'session_key': self.user_or_session_key}

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
                **filter_kwargs
            )


class DeleteCartFromPacketLogic:
    def __init__(self, is_authenticated: bool, cart_id, user_or_session_key):
        self.is_authenticated = is_authenticated
        self.cart_id = cart_id
        self.user_or_session_key = user_or_session_key

    def delete_cart_packet(self):
        cart = Cart.objects.get(pk=self.cart_id)
        cart.delete()

        filter_kwargs_user = {"user": self.user_or_session_key} if self.is_authenticated else\
                             {"session_key": self.user_or_session_key}

        carts_left = Cart.objects.filter(**filter_kwargs_user)

        new_quantity = sum([item.quantity for item in carts_left])

        return new_quantity


class ChangeCartQuantity:
    def __init__(self, is_authenticated, is_plus, cart_id, user_or_session_key):
        self.is_authenticated = is_authenticated
        self.is_plus = is_plus
        self.cart_id = cart_id
        self.user_or_session_key = user_or_session_key

    def change_cart_quantity(self):
        cart = Cart.objects.get(pk=self.cart_id)

        user_filter = {"user": self.user_or_session_key} if self.is_authenticated else \
                      {"session_key": self.user_or_session_key}

        if self.is_plus == "false":
            cart.quantity = cart.quantity - 1
            if cart.quantity == 0:
                cart.delete()
            else:
                cart.save()
        else:
            cart.quantity = cart.quantity + 1
            cart.save()

        carts_left = Cart.objects.filter(**user_filter)

        new_quantity = sum([item.quantity for item in carts_left])

        return new_quantity

