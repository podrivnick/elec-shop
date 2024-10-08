from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass


@dataclass
class BaseQueryGetUserModelService(ABC):
    @abstractmethod
    def get_usermodel_by_username(self):
        raise NotImplementedError()
