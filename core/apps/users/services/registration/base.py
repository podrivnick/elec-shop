from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass


@dataclass
class BaseQueryUserInNotExistService(ABC):
    @abstractmethod
    def verificate_user(self):
        raise NotImplementedError()


@dataclass
class BaseCommandCreateUserService(ABC):
    @abstractmethod
    def create_user(self):
        raise NotImplementedError()
