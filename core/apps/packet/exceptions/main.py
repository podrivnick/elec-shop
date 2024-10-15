from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.infrastructure.exceptions.base import DomainException


@dataclass(frozen=True, eq=False)
class DatabaseCartError(DomainException):
    exception: Optional[str] = field(default="Error checking Favorite")

    @property
    def message(self) -> Optional[str]:
        return self.exception
