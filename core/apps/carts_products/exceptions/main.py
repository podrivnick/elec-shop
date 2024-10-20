from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.infrastructure.exceptions.base import DomainException


@dataclass(frozen=True, eq=False)
class UserAlreadyWriteReviewError(DomainException):
    exception: Optional[str] = field(default="User Already Write Review.")

    @property
    def message(self) -> Optional[str]:
        return self.exception
