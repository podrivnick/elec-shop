import re
from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.apps.common.domain.base import ValueObject
from core.infrastructure.exceptions.base import DomainException


MAX_ADDRESS_LENGTH = 120
ADDRESS_PATTERN = re.compile(r"^[A-Z][a-zA-Z'-]*$")


@dataclass(frozen=True, eq=False)
class BaseDeliveryAddressException(ValueError, DomainException):
    address: Optional[str] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class EmptyDeliveryAddressException(BaseDeliveryAddressException):
    exception: Optional[str] | None = field(default="Empty address name")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class TooLongDeliveryAddressException(BaseDeliveryAddressException):
    exception: Optional[str] | None = field(default="Too long address")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class WrongDeliveryAddressFormatException(BaseDeliveryAddressException):
    exception: Optional[str] | None = field(default="Wrong address format")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class DeliveryAddress(ValueObject[str | None]):
    value: str | None

    def validate(self) -> None:
        if self.value is None:
            return

        if len(self.value) == 0:
            raise EmptyDeliveryAddressException(self.value)

        if len(self.value) > MAX_ADDRESS_LENGTH:
            raise TooLongDeliveryAddressException(self.value)

        # if not ADDRESS_PATTERN.match(self.value): noqa
        #     raise WrongDeliveryAddressFormatException(self.value)

    def exists(self) -> bool:
        return self.value is not None
