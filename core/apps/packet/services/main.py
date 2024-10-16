from dataclasses import dataclass
from typing import (
    Dict,
    List,
    Optional,
    Tuple,
)

from django.db.models import QuerySet

from core.apps.main.entities.product import ProductEntity
from core.apps.main.models.products import Products
from core.apps.packet.entities.cart import CartEntity
from core.apps.packet.exceptions.main import DatabaseCartError
from core.apps.packet.models.cart import Cart
from core.apps.packet.repositories.base import BaseCommandUpdateCartRepository
from core.apps.packet.services.base import (
    BaseCommandUpdateDataCartService,
    BaseQueryGetCartService,
    BaseQueryGetProductService,
)
from core.apps.users.models import User


@dataclass
class ORMQueryGetProductService(BaseQueryGetProductService):
    def get_product_by_id(
        self,
        id_product: Optional[int],
    ) -> ProductEntity:
        product = Products.objects.get(id_product=id_product)

        return product


@dataclass
class ORMQueryGetCartService(BaseQueryGetCartService):
    def get_cart_by_id(self, cart_id: Optional[int]):
        return Cart.objects.filter(pk=cart_id).first()

    def get_cart_by_product_and_user(
        self,
        product: ProductEntity,
        filters: Dict[str, QuerySet[User] | str],
    ) -> QuerySet[Cart]:
        return Cart.objects.filter(
            product__id_product=product.id_product,
            **filters,
        ).first()

    def get_all_carts_by_user(
        self,
        filters: Dict[str, QuerySet[User] | str],
    ) -> Tuple[CartEntity, int]:
        carts = Cart.objects.filter(
            **filters,
        )

        packet_entity = [
            self.create_cart_entity(filtered_cart) for filtered_cart in carts
        ]
        total_quantity = self.calculate_total_quantity(packet_entity)

        return (packet_entity, total_quantity)

    @staticmethod
    def create_cart_entity(filtered_cart: QuerySet[Cart]) -> CartEntity:
        return CartEntity(
            pk=filtered_cart.pk,
            user=filtered_cart.user if filtered_cart.user else None,
            session_key=filtered_cart.session_key if not filtered_cart.user else None,
            product=ProductEntity(
                id_product=filtered_cart.product.id_product,
                name=filtered_cart.product.name,
                description=filtered_cart.product.description,
                slug=filtered_cart.product.slug,
                image=filtered_cart.product.image,
                discount=filtered_cart.product.discount,
                price=filtered_cart.product.price,
                count_product=filtered_cart.product.count_product,
                category=filtered_cart.product.category,
                created_at=filtered_cart.product.created_at,
                updated_at=filtered_cart.product.updated_at,
            ),
            quantity=filtered_cart.quantity,
        )

    @staticmethod
    def calculate_total_quantity(
        packet_entity: List[CartEntity],
    ) -> int:
        total_quantity = sum(item.quantity for item in packet_entity)
        return total_quantity


@dataclass
class CommandUpdateDataCartService(BaseCommandUpdateDataCartService):
    command_update_cart: BaseCommandUpdateCartRepository

    def update_or_create_cart(
        self,
        packet: QuerySet[Cart],
        product: ProductEntity,
        filters: Dict[str, QuerySet[User] | str],
    ) -> QuerySet[Cart]:
        if packet:
            packet = self.command_update_cart.increase_quantity_products(packet=packet)
        else:
            packet = self.command_update_cart.create_cart(
                product=product,
                filters=filters,
            )

        packet_entity = CartEntity(
            pk=packet.pk,
            user=packet.user if packet.user else None,
            session_key=packet.session_key if not packet.user else None,
            product=ProductEntity(
                id_product=packet.product.id_product,
                name=packet.product.name,
                description=packet.product.description,
                slug=packet.product.slug,
                image=packet.product.image,
                discount=packet.product.discount,
                price=packet.product.price,
                count_product=packet.product.count_product,
                category=packet.product.category,
                created_at=packet.product.created_at,
                updated_at=packet.product.updated_at,
            ),
            quantity=packet.quantity,
        )

        return packet_entity

    def delete_cart_from_packet(
        self,
        cart_id: int,
    ) -> None:
        cart = Cart.objects.get(pk=cart_id)
        cart.delete()

    def process_change_quantity_products_in_packet(
        self,
        cart_id: Optional[int],
        is_plus: Optional[str],
        cart: QuerySet[Cart],
    ) -> None:
        try:
            cart = Cart.objects.get(pk=cart_id)
            self._change_quantity(is_plus=is_plus, cart=cart, cart_id=cart_id)
        except Cart.DoesNotExist:
            raise DatabaseCartError("Not Found Cart")

    def _change_quantity(
        self,
        cart_id: Optional[int],
        is_plus: Optional[str],
        cart: QuerySet[Cart],
    ) -> None:
        """Обновляем количество товара в корзине на основе значения is_plus."""
        change_value = -1 if is_plus == "false" else 1
        new_quantity = cart.quantity + change_value

        if new_quantity <= 0:
            cart.delete()
        else:
            self.command_update_cart.change_quantity_products(
                cart_id=cart_id,
                change_value=change_value,
            )
