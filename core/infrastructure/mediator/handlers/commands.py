from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Any,
    Generic,
    TypeVar,
)

from core.infrastructure.mediator.base import BaseCommands


CT = TypeVar("CT", bound=BaseCommands)
CR = TypeVar("CR", bound=Any)


@dataclass(frozen=True)
class CommandHandler(ABC, Generic[CT, CR]):
    @abstractmethod
    def handle(self, command: CT) -> CR:
        raise NotImplementedError("Subclasses must implement handle method")
