from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import Tuple

from django.db.models import QuerySet

from core.apps.packet.entities.cart import CartEntity
from core.apps.packet.models.cart import Cart


@dataclass
class BaseQueryGetProductService(ABC):
    @abstractmethod
    def get_product_by_id(self):
        raise NotImplementedError()


@dataclass
class BaseQueryGetCartService(ABC):
    @abstractmethod
    def get_cart_by_product_and_user(self) -> QuerySet[Cart]:
        raise NotImplementedError()

    @abstractmethod
    def get_all_carts_by_user(self) -> Tuple[CartEntity, int]:
        raise NotImplementedError()

    @abstractmethod
    def get_cart_by_id(self):
        raise NotImplementedError()


@dataclass
class BaseCommandUpdateDataCartService(ABC):
    @abstractmethod
    def update_or_create_cart(self) -> QuerySet[Cart]:
        raise NotImplementedError()

    @abstractmethod
    def delete_cart_from_packet(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def process_change_quantity_products_in_packet(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _change_quantity(self) -> None:
        raise NotImplementedError()
