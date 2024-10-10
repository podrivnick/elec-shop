from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass


@dataclass
class BaseCommandLogoutUserService(ABC):
    @abstractmethod
    def logout_user(self):
        raise NotImplementedError()
