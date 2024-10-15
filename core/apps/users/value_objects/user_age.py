import re
from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.apps.common.domain.base import ValueObject
from core.infrastructure.exceptions.base import DomainException


MAX_AGE_USER_LENGTH = 90
MIN_AGE_USER_LENGTH = 18
AGE_USER_PATTERN = re.compile(r"^(1[89]|[2-8]\d|90)$")


@dataclass(frozen=True, eq=False)
class BaseAgeUserException(ValueError, DomainException):
    age_user: Optional[str] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class EmptyAgeUserException(BaseAgeUserException):
    exception: Optional[str] | None = field(default="Empty age user")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class TooMuchAgeUserException(BaseAgeUserException):
    exception: Optional[str] | None = field(default="Too long age of user")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class TooSmallAgeUserException(BaseAgeUserException):
    exception: Optional[str] | None = field(default="Too small age of user")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class WrongAgeUserFormatException(BaseAgeUserException):
    exception: Optional[str] | None = field(default="Wrong age user format")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class AgeUser(ValueObject[str | None]):
    value: str | None

    def validate(self) -> None:
        if not self.value:
            return

        if not self.value:
            raise EmptyAgeUserException(self.value)

        if int(self.value) > MAX_AGE_USER_LENGTH:
            raise TooMuchAgeUserException(self.value)

        if int(self.value) < MIN_AGE_USER_LENGTH:
            raise TooSmallAgeUserException(self.value)

        if not isinstance(int(self.value), int):
            raise WrongAgeUserFormatException(self.value)

    def exists(self) -> bool:
        return self.value is not None
