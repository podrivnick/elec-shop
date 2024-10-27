from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.apps.common.domain.base import ValueObject
from core.apps.orders.utils.spec import IsNumericTotalPriceSpec
from core.apps.orders.utils.validators import (
    IsNotEmptySpec,
    IsNumbericCorrectFormat,
)
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
        total_price_spec = (
            IsNumericTotalPriceSpec()
            .and_spec(IsNotEmptySpec())
            .and_spec(IsNumbericCorrectFormat())
        )

        total_price_spec.is_satisfied(self.value)

    def exists(self) -> bool:
        return self.value is not None
