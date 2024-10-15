from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from django.db.models import QuerySet

from core.apps.packet.models.cart import Cart


@dataclass
class BaseCommandUpdateCartRepository(ABC):
    @abstractmethod
    def increase_quantity_products(self) -> QuerySet[Cart]:
        raise NotImplementedError()

    @abstractmethod
    def create_cart(self) -> QuerySet[Cart]:
        raise NotImplementedError()

    @abstractmethod
    def change_quantity_products(self) -> None:
        raise NotImplementedError()
