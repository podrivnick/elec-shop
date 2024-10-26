from dataclasses import dataclass
from typing import Optional

from django.db.models import QuerySet

from core.apps.main.models.products import Products
from core.apps.orders.models.orders import (
    OrderItem,
    Orders,
)
from core.apps.orders.repositories.base import BaseCommandOrderRepository


@dataclass(frozen=True, eq=False)
class ORMBaseCommandOrderRepository(BaseCommandOrderRepository):
    def create_order_items(
        self,
        order: QuerySet[Orders],
        product: QuerySet[Products],
        name: Optional[str],
        price: Optional[int],
        quantity: Optional[int],
    ) -> None:
        OrderItem.objects.create(
            order=order,
            product=product,
            name=name,
            price=price,
            quantity=quantity,
        )

    def delete_basic_order(
        self,
        order: QuerySet[Orders],
    ) -> None:
        order.delete()
