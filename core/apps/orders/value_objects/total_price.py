from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.apps.common.domain.base import ValueObject
from core.infrastructure.exceptions.base import DomainException


MAX_TOTAL_PRICE_LENGTH = 120


@dataclass(frozen=True, eq=False)
class BaseTotalPriceException(ValueError, DomainException):
    total_price: Optional[str] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class EmptyTotalPriceException(BaseTotalPriceException):
    exception: Optional[str] | None = field(default="Empty address name")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class TooLongTotalPriceException(BaseTotalPriceException):
    exception: Optional[str] | None = field(default="Too long address")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class WrongTotalPriceFormatException(BaseTotalPriceException):
    exception: Optional[str] | None = field(default="Wrong address format")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class TotalPrice(ValueObject[str | None]):
    value: str | None

    def validate(self) -> None:
        if self.value is None:
            return

        # if len(self.value) == 0:
        #     raise EmptyTotalPriceException(self.value)

        # if len(self.value) > MAX_TOTAL_PRICE_LENGTH:
        #     raise TooLongTotalPriceException(self.value)

        # if not ADDRESS_PATTERN.match(self.value): noqa
        #     raise WrongTotalPriceFormatException(self.value)

    def exists(self) -> bool:
        return self.value is not None
