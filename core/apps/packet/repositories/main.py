from dataclasses import dataclass
from typing import Dict

from django.db.models import QuerySet

from core.apps.main.models.products import Products
from core.apps.packet.models.cart import Cart
from core.apps.packet.repositories.base import BaseCommandUpdateCartRepository
from core.apps.users.models import User


@dataclass
class ORMCommandUpdateCartRepository(BaseCommandUpdateCartRepository):
    def increase_quantity_products(
        self,
        packet: QuerySet[Cart],
    ) -> QuerySet[Cart]:
        packet.quantity += 1
        packet.save()

        return packet

    def create_cart(
        self,
        product: QuerySet[Products],
        filters: Dict[str, QuerySet[User] | str],
    ) -> None:
        return Cart.objects.create(
            product=product,
            quantity=1,
            **filters,
        )
