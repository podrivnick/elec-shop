import re
from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.apps.common.domain.base import ValueObject
from core.infrastructure.exceptions.base import DomainException


MAX_LASTNAME_LENGTH = 50
LASTNAME_PATTERN = re.compile(r"^[A-Z][a-zA-Z'-]*$")


@dataclass(frozen=True, eq=False)
class BaseLastNameException(ValueError, DomainException):
    last_name: Optional[str] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class EmptyLastNameException(BaseLastNameException):
    exception: Optional[str] | None = field(default="Empty last name")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class TooLongLastNameException(BaseLastNameException):
    exception: Optional[str] | None = field(default="Too long last name")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class WrongLastNameFormatException(BaseLastNameException):
    exception: Optional[str] | None = field(default="Wrong last name format")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class LastName(ValueObject[str | None]):
    value: str | None

    def validate(self) -> None:
        if self.value is None:
            return

        if len(self.value) == 0:
            raise EmptyLastNameException(self.value)

        if len(self.value) > MAX_LASTNAME_LENGTH:
            raise TooLongLastNameException(self.value)

        if not LASTNAME_PATTERN.match(self.value):
            raise WrongLastNameFormatException(self.value)

    def exists(self) -> bool:
        return self.value is not None
