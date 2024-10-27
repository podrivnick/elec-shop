import re
from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.apps.common.domain.base import ValueObject
from core.apps.orders.utils.spec import IsStringSpec
from core.apps.orders.utils.validators import (
    IsNotEmptySpec,
    IsValidEmailSpec,
    MaxLengthSpec,
)
from core.infrastructure.exceptions.base import DomainException


MAX_EMAIL_LENGTH = 50
EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


@dataclass(frozen=True, eq=False)
class BaseEmailException(ValueError, DomainException):
    email: Optional[str] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class EmptyEmailException(BaseEmailException):
    exception: Optional[str] | None = field(default="Empty email name")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class TooLongEmailException(BaseEmailException):
    exception: Optional[str] | None = field(default="Too long email name")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class WrongEmailFormatException(BaseEmailException):
    exception: Optional[str] | None = field(default="Wrong email name format")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class Email(ValueObject[str | None]):
    value: str | None

    def validate(self) -> None:
        email_spec = (
            IsStringSpec()
            .and_spec(IsNotEmptySpec())
            .and_spec(MaxLengthSpec(MAX_EMAIL_LENGTH))
            .and_spec(IsValidEmailSpec())
        )

        email_spec.is_satisfied(self.value)

    def exists(self) -> bool:
        return self.value is not None
