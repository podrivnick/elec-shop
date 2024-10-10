from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.infrastructure.exceptions.base import DomainException


@dataclass(eq=False)
class AuthenticationError(DomainException):
    exception: Optional[str] | None = field(default="Authentication Error")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(eq=False)
class UserNotFoundError(DomainException):
    exception: Optional[str] | None = field(default="User not found")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(eq=False)
class LogoutUserError(DomainException):
    exception: Optional[str] | None = field(default="User not logouted")

    @property
    def message(self) -> Optional[str]:
        return self.exception
