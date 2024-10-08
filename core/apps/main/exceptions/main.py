from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.infrastructure.exceptions.base import DomainException


@dataclass(frozen=True, eq=False)
class DatabaseFavoriteError(DomainException):
    exception: Optional[str] = field(default="Error checking Favorite")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class FavoriteProductError(DomainException):
    exception: Optional[str] = field(default="Error changing Favorite")

    @property
    def message(self) -> Optional[str]:
        return self.exception
