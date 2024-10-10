from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.infrastructure.exceptions.base import DomainException


@dataclass(eq=False)
class UserNotVerifiedError(DomainException):
    exception: Optional[str] = field(default="User Not Verified")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass
class UserNotAuthenticatedError(DomainException):
    exception: Optional[str] = field(default="User Not Authenticated")

    @property
    def message(self) -> Optional[str]:
        return self.exception
