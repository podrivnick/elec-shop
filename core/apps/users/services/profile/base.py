from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass


@dataclass
class BaseQueryFilterCartsByUserService(ABC):
    @abstractmethod
    def get_carts_user(self):
        raise NotImplementedError()
