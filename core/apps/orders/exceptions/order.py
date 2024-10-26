from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.apps.orders.config import (
    MISTAKE_BASE_CLASS_EXCEPTION,
    NOT_ENOUGH_COUNT_PRODUCTS,
)
from core.infrastructure.exceptions.base import DomainException


@dataclass
class BaseOrderException(Exception):
    @property
    def exception(self):
        return f"{MISTAKE_BASE_CLASS_EXCEPTION}"


@dataclass
class ExceptionNotEnoughQuantityProduct(BaseOrderException):
    name_product: str

    @property
    def exception(self):
        return f"{NOT_ENOUGH_COUNT_PRODUCTS}{self.name_product}"


@dataclass(frozen=True, eq=False)
class OrderNotCreatedError(DomainException):
    exception: Optional[str] = field(default="Couldn't create an order.")

    @property
    def message(self) -> Optional[str]:
        return self.exception
