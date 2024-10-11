import re
from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.apps.common.domain.base import ValueObject
from core.infrastructure.exceptions.base import DomainException


MAX_FIRSTNAME_LENGTH = 32
FIRSTNAME_PATTERN = re.compile(r"^[A-Z][a-zA-Z'-]*$")


@dataclass(frozen=True, eq=False)
class BaseFirstNameException(ValueError, DomainException):
    first_name: Optional[str] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class EmptyFirstNameException(BaseFirstNameException):
    exception: Optional[str] | None = field(default="Empty first name")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class TooLongFirstNameException(BaseFirstNameException):
    exception: Optional[str] | None = field(default="Too long first name")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class WrongFirstNameFormatException(BaseFirstNameException):
    exception: Optional[str] | None = field(default="Wrong first name format")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class FirstName(ValueObject[str | None]):
    value: str | None

    def validate(self) -> None:
        if self.value is None:
            return

        if len(self.value) == 0:
            raise EmptyFirstNameException(self.value)

        if len(self.value) > MAX_FIRSTNAME_LENGTH:
            raise TooLongFirstNameException(self.value)

        if not FIRSTNAME_PATTERN.match(self.value):
            raise WrongFirstNameFormatException(self.value)

    def exists(self) -> bool:
        return self.value is not None
