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


@dataclass(frozen=True, eq=False)
class UserAlreadyWriteLikedReviewError(DomainException):
    exception: Optional[str] = field(default="User Already Liked Review.")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class ReviewNotFoundError(DomainException):
    exception: Optional[str] = field(default="Review Not Exist.")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class ProductNotFoundError(DomainException):
    exception: Optional[str] = field(default="Product Not Exist.")

    @property
    def message(self) -> Optional[str]:
        return self.exception
