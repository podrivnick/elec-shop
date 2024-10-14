from dataclasses import dataclass
from typing import (
    Dict,
    Optional,
)

from django.db.models import QuerySet

from core.apps.main.entities.product import ProductEntity
from core.apps.main.models.products import Products
from core.apps.packet.entities.cart import CartEntity
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
        # return ProductEntity(
        #     id_product=product.id_product,
        #     name=product.name,
        #     description=product.description,
        #     slug=product.slug,
        #     image=product.image,
        #     discount=product.discount,
        #     price=product.price,
        #     count_product=product.count_product,
        #     category=product.category,
        #     created_at=product.created_at,
        #     updated_at=product.updated_at,
        # )


@dataclass
class ORMQueryGetCartService(BaseQueryGetCartService):
    def get_cart_by_product_and_user(
        self,
        product: ProductEntity,
        filters: Dict[str, QuerySet[User] | str],
    ) -> QuerySet[Products]:
        return Cart.objects.filter(
            product__id_product=product.id_product,
            **filters,
        ).first()


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
            user=packet.user,
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
