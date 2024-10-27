import re
from dataclasses import (
    dataclass,
    field,
)
from typing import Pattern

from core.apps.orders.exceptions.order import (
    DeliveryAddressNotAllowedSymbolsException,
    OrderDataIsEmptyException,
    OrderDataIsNotAlphabeticException,
    OrderDataTooLongError,
    OrderDataTotalPriceIncorrectFormatError,
)
from core.apps.orders.utils.spec import Specification
from core.apps.users.exceptions.main import (
    IncorrectFormatEmailException,
    IncorrectFormatPhoneException,
)


# max length  noqa
@dataclass(frozen=True)
class MaxLengthSpec(Specification):
    max_length: int = field(default=120)

    def is_satisfied(
        self,
        item: str,
    ) -> bool:
        if len(item) > self.max_length:
            raise OrderDataTooLongError()
        return True


# not empty  noqa
@dataclass(frozen=True)
class IsNotEmptySpec(Specification):
    def is_satisfied(
        self,
        item: str,
    ) -> bool:
        if not bool(item.strip()):
            raise OrderDataIsEmptyException()
        return True


# only alpha  noqa
@dataclass(frozen=True)
class IsAlphabeticSpec(Specification):
    def is_satisfied(
        self,
        item: str,
    ) -> bool:
        if not item.replace(" ", "").isalpha():
            raise OrderDataIsNotAlphabeticException()
        return True


@dataclass(frozen=True)
class IsNumbericCorrectFormat(Specification):
    _total_price_pattern: Pattern[str] = field(
        default_factory=lambda: re.compile(r"^[1-9]\d*(\.\d+)?$"),
    )

    def is_satisfied(
        self,
        item: str,
    ) -> bool:
        if not bool(re.match(self._total_price_pattern, item)):
            raise OrderDataTotalPriceIncorrectFormatError()
        return True


# Spec for delivery address  noqa
@dataclass(frozen=True)
class NoSpecialCharactersSpec(Specification):
    _forbidden_chars: str = field(default="!@#$%^&*()[]{};:'\"<>?\\|`~")

    def is_satisfied(
        self,
        item: str,
    ) -> bool:
        if any(char in self._forbidden_chars for char in item):
            raise DeliveryAddressNotAllowedSymbolsException()
        return True


@dataclass(frozen=True)
class IsValidEmailSpec(Specification):
    _email_pattern: Pattern[str] = field(
        default_factory=lambda: re.compile(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        ),
    )

    def is_satisfied(
        self,
        item: str,
    ) -> bool:
        if not re.match(
            self._email_pattern,
            item,
        ):
            raise IncorrectFormatEmailException()
        return True


@dataclass(frozen=True)
class IsValidPhoneSpec(Specification):
    _phone_pattern: Pattern[str] = field(
        default_factory=lambda: re.compile(r"^\+?[1-9]\d{9,14}$"),
    )

    def is_satisfied(
        self,
        item: str,
    ) -> bool:
        if not re.match(
            self._phone_pattern,
            item,
        ):
            raise IncorrectFormatPhoneException()
        return True
