from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Dict,
    Self,
)

from core.apps.common.domain.base import Entity
from core.apps.orders import value_objects as vo_orders
from core.apps.users import value_objects as vo


@dataclass(frozen=True, eq=False)
class Order(Entity):
    first_name: vo.FirstName | None = field(default=None)
    last_name: vo.LastName | None = field(default=None)
    email: vo.Email | None = field(default=None)
    phone: vo.PhoneNumber | None = field(default=None)
    delivery_address: vo_orders.DeliveryAddress | None = field(default=None)
    total_price: vo_orders.TotalPrice | None = field(default=None)
    payment_on_get: bool = field(default=False)
    required_delivery: bool = field(default=True)

    @classmethod
    def create_order_entity(
        cls,
        first_name: vo.FirstName = None,
        last_name: vo.LastName = None,
        email: vo.Email = None,
        phone: vo.PhoneNumber = None,
        delivery_address: vo_orders.DeliveryAddress = None,
        total_price: vo_orders.TotalPrice = None,
        payment_on_get: bool = False,
        required_delivery: bool = True,
    ) -> Self:
        order = cls(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            delivery_address=delivery_address,
            required_delivery=required_delivery,
            payment_on_get=payment_on_get,
            total_price=total_price,
        )

        return order

    def to_dict(self) -> Dict:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "delivery_address": self.delivery_address,
            "required_delivery": self.required_delivery,
            "payment_on_get": self.payment_on_get,
            "total_price": self.total_price,
        }
