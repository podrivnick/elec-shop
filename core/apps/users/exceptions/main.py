from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.infrastructure.exceptions.base import DomainException


@dataclass(frozen=True, eq=False)
class UserNotVerifiedError(DomainException):
    exception: Optional[str] = field(default="User Not Verified")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class UserNotAuthenticatedError(DomainException):
    exception: Optional[str] = field(default="User Not Authenticated")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class UserPasswordsIsNotEqual(DomainException):
    exception: Optional[str] = field(default="Passwords not equal")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class UserUpdatedDataNotValidated(DomainException):
    exception: Optional[str] = field(default="Invalid New Information")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class IncorrectFormatEmailException(DomainException):
    exception: Optional[str] = field(default="Invalid Email")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class IncorrectFormatPhoneException(DomainException):
    exception: Optional[str] = field(default="Invalid Phone")

    @property
    def message(self) -> Optional[str]:
        return self.exception
