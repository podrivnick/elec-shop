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


@dataclass(frozen=True, eq=False)
class OrderDataTooLongError(DomainException):
    exception: Optional[str] = field(default="Order data too long.")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class OrderDataIsEmptyException(DomainException):
    exception: Optional[str] = field(default="Order data is empty.")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class OrderDataIsNotAlphabeticException(DomainException):
    exception: Optional[str] = field(default="Order data is not alphabetic error.")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class OrderDataContainsNotOnlyDigitsException(DomainException):
    exception: Optional[str] = field(
        default="Order data contains not only digits error.",
    )

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class OrderDataTotalPriceIncorrectFormatError(DomainException):
    exception: Optional[str] = field(
        default="Order data total price incorrect format error.",
    )

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class DeliveryAddressNotAllowedSymbolsException(DomainException):
    exception: Optional[str] = field(
        default="Order data delivery address format error.",
    )

    @property
    def message(self) -> Optional[str]:
        return self.exception
