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


@dataclass
class BaseCommandSetUpdatedInformationOfUserService(ABC):
    @abstractmethod
    def set_information_user(self):
        raise NotImplementedError()


@dataclass
class BaseQueryValidateNewDataService(ABC):
    @abstractmethod
    def validate_new_information_user(self):
        raise NotImplementedError()
