from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from typing import (
    Dict,
    Optional,
)

from core.apps.common.schemas.base import Schema
from core.apps.main.entities.product import ProductEntity


@dataclass(frozen=True, eq=False)
class OrderSchema(Schema):
    first_name: Optional[str] | None = field(default=None)
    last_name: Optional[str] | None = field(default=None)
    email: Optional[str] | None = field(default=None)
    phone: Optional[str] | None = field(default=None)
    delivery_address: Optional[str] | None = field(default=None)
    required_delivery: Optional[bool] | None = field(default=False)
    payment_on_get: Optional[int] | None = field(default=False)

    def to_dict(self) -> Dict:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "delivery_address": self.delivery_address,
            "required_delivery": self.required_delivery,
            "payment_on_get": self.payment_on_get,
        }


@dataclass(frozen=True, eq=False)
class OrderItemSchema(Schema):
    created_timestamp: datetime
    pk: Optional[int] | None = field(default=None)
    order: OrderSchema | None = field(default=None)
    product: ProductEntity | None = field(default=None)
    name: Optional[str] | None = field(default=None)
    price: Optional[int] | None = field(default=None)
    quantity: Optional[int] | None = field(default=None)

    @property
    def products_price(self):
        return round(self.product.sell_price() * self.quantity, 2)
