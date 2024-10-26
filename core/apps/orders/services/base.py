from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from django.db.models import QuerySet

from core.apps.orders.models.orders import Orders


@dataclass
class BaseCommandOrderService(ABC):
    @abstractmethod
    def create_basic_order(self) -> QuerySet[Orders]:
        raise NotImplementedError()

    @abstractmethod
    def create_orders_items(self) -> None:
        raise NotImplementedError()


@dataclass
class BaseQueryValidationOrderService(ABC):
    @abstractmethod
    def validate_order_data(self) -> None:
        raise NotImplementedError()
