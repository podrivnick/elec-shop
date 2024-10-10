import re
from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.apps.common.domain.base import ValueObject
from core.infrastructure.exceptions.base import DomainException


MAX_USERNAME_LENGTH = 32
USERNAME_PATTERN = re.compile(r"[A-Za-z][A-Za-z1-9_]+")


@dataclass(frozen=True, eq=False)
class BaseUsernameException(ValueError, DomainException):
    username: Optional[str] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class EmptyUsernameException(BaseUsernameException):
    exception: Optional[str] | None = field(default="Empty username")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class TooLongUsernameException(BaseUsernameException):
    exception: Optional[str] | None = field(default="Too long username")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class WrongUsernameFormatException(BaseUsernameException):
    exception: Optional[str] | None = field(default="Wrong username format")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class UserName(ValueObject[str | None]):
    value: str | None

    def validate(self) -> None:
        if self.value is None:
            return

        if len(self.value) == 0:
            raise EmptyUsernameException(self.value)

        if len(self.value) > MAX_USERNAME_LENGTH:
            raise TooLongUsernameException(self.value)

        if not USERNAME_PATTERN.match(self.value):
            raise WrongUsernameFormatException(self.value)

    def exists(self) -> bool:
        return self.value is not None
