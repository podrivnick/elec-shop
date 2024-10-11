import re
from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.apps.common.domain.base import ValueObject
from core.infrastructure.exceptions.base import DomainException


MAX_LENGTH_PASSWORD = 32
PASSWORD_PATTERN = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")


@dataclass(frozen=True, eq=False)
class BasePasswordException(ValueError, DomainException):
    password: Optional[str] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class EmptyPasswordException(BasePasswordException):
    exception: Optional[str] | None = field(default="Empty password")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class TooLongPasswordException(BasePasswordException):
    exception: Optional[str] | None = field(default="Too long password")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class WrongPasswordException(BasePasswordException):
    exception: Optional[str] | None = field(default="Wrong password format")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class Password(ValueObject[str | None]):
    value: str | None

    def validate(self) -> None:
        if not self.exists():
            return

        if len(self.value) == 0:
            raise EmptyPasswordException(self.value)

        if len(self.value) > MAX_LENGTH_PASSWORD:
            raise TooLongPasswordException(self.value)

        if not PASSWORD_PATTERN.match(self.value):
            raise WrongPasswordException(self.value)

    def exists(self) -> bool:
        return self.value is not None
