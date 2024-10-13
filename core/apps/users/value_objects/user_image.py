import re
from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.apps.common.domain.base import ValueObject
from core.infrastructure.exceptions.base import DomainException


IMAGE_USER_PATTERN = re.compile(r"^avatars/\d{4}/\d{2}/\d{2}/[\w-]+_[\w]+\.\w{3,4}$")


@dataclass(frozen=True, eq=False)
class BaseImageUserException(ValueError, DomainException):
    image_user: Optional[str] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class EmptyImageUserException(BaseImageUserException):
    exception: Optional[str] | None = field(default="Empty image user")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class TooLongImageUserException(BaseImageUserException):
    exception: Optional[str] | None = field(default="Too long image user")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class WrongImageUserFormatException(BaseImageUserException):
    exception: Optional[str] | None = field(default="Wrong image user format")

    @property
    def message(self) -> Optional[str]:
        return self.exception


@dataclass(frozen=True, eq=False)
class ImageUser(ValueObject[str | None]):
    value: str | None

    def validate(self) -> None:
        if self.value is None:
            return

        # if not IMAGE_USER_PATTERN.match(str(self.value)):
        #     raise WrongImageUserFormatException(self.value)

    def exists(self) -> bool:
        return self.value is not None
