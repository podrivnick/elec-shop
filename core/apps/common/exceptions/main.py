from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.infrastructure.exceptions.base import DomainException


@dataclass(frozen=True, eq=False)
class AuthenticationError(DomainException):
    exception: Optional[str] | None = field(default="Authentication Error")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class UserNotFoundError(DomainException):
    exception: Optional[str] | None = field(default="User not found")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class LogoutUserError(DomainException):
    exception: Optional[str] | None = field(default="User not logouted")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class UserNotFoundByUsername(DomainException):
    exception: Optional[str] | None = field(default="Username incorrect")

    @property
    def message(self) -> Optional[str]:
        return self.exception
