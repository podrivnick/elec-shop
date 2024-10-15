from typing import (
    Dict,
    List,
)

from core.apps.main.entities.product import ProductEntity
from core.apps.main.utils.main import GetUserModel
from core.apps.packet.entities.cart import CartEntity
from core.apps.packet.models.cart import Cart


def create_cart_entity(item) -> CartEntity:
    """Создаем сущность корзины на основе модели Cart."""
    return CartEntity(
        pk=item.pk,
        user=item.user if item.user else None,
        session_key=item.session_key if not item.user else None,
        product=ProductEntity(
            id_product=item.product.id_product,
            name=item.product.name,
            description=item.product.description,
            slug=item.product.slug,
            image=item.product.image,
            discount=item.product.discount,
            price=item.product.price,
            count_product=item.product.count_product,
            category=item.product.category,
            created_at=item.product.created_at,
            updated_at=item.product.updated_at,
        ),
        quantity=item.quantity,
    )


def calculate_totals(packet_entity: List[CartEntity]) -> Dict[str, int]:
    """Вычисляем общую стоимость и количество товаров."""
    total_price = sum(item.products_price for item in packet_entity)
    total_quantity = sum(item.quantity for item in packet_entity)
    return {
        "total_price": total_price,
        "total_quantity": total_quantity,
    }


def get_filtered_carts(user, session_key) -> List[Cart]:
    """Получаем корзину на основе пользователя или сессии."""
    if user.is_authenticated:
        return (
            Cart.objects.filter(user=user)
            .select_related("product")
            .order_by("-quantity")
        )
    else:
        return Cart.objects.filter(session_key=session_key).order_by("-quantity")


def get_carts(request) -> Dict[str, CartEntity | int]:
    """Основная функция для получения данных корзины."""
    if not request.session.session_key:
        request.session.create()

    filtered_carts = get_filtered_carts(request.user, request.session.session_key)

    packet_entity = [create_cart_entity(item) for item in filtered_carts]

    totals = calculate_totals(packet_entity)

    return {
        "packet": packet_entity,
        **totals,  # Включаем total_price и total_quantity в результат
    }


class UserOrSessionKeyMixin:
    def get_user_or_created_session_key(self):
        if self.request.user.is_authenticated:
            user_model = GetUserModel(self.request.user)
            user = user_model.get_user_model()

            return user, True
        else:
            return self.request.session.session_key, False
