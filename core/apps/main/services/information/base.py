from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass


@dataclass
class BaseQueryFAQInformationService(ABC):
    @abstractmethod
    def get_all_information(self):
        raise NotImplementedError()
