from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class BaseCommandOrderRepository(ABC):
    @abstractmethod
    def create_order_items(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete_basic_order(self) -> None:
        raise NotImplementedError()
