from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True, eq=False)
class BaseAppException(Exception):
    """Base class for app exceptions."""

    status: ClassVar[int] = 500

    @property
    def message(self) -> str:
        return "Some Exception in App"


@dataclass(frozen=True, eq=False)
class DomainException(BaseAppException):
    """Base class for domain exceptions."""

    @property
    def message(self) -> str:
        return "Domain exception occured"
