import re
from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.apps.common.domain.base import ValueObject
from core.infrastructure.exceptions.base import DomainException


MAX_PHONE_LENGTH = 32
PHONE_PATTERN = re.compile(r"^\+380\d{9}$")


@dataclass(frozen=True, eq=False)
class BasePhoneUserException(ValueError, DomainException):
    phone_number: Optional[str] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class EmptyPhoneNumberException(BasePhoneUserException):
    exception: Optional[str] | None = field(default="Empty phone name")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class TooPhoneNumberNameException(BasePhoneUserException):
    exception: Optional[str] | None = field(default="Too long phone number")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class WrongPhoneNumberFormatException(BasePhoneUserException):
    exception: Optional[str] | None = field(default="Wrong phone format")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class PhoneNumber(ValueObject[str | None]):
    value: str | None

    def validate(self) -> None:
        if self.value == "0":
            return

        if len(self.value) == 0:
            raise EmptyPhoneNumberException(self.value)

        if len(self.value) > MAX_PHONE_LENGTH:
            raise TooPhoneNumberNameException(self.value)

        if not PHONE_PATTERN.match(self.value):
            raise WrongPhoneNumberFormatException(self.value)

    def exists(self) -> bool:
        return self.value is not None
