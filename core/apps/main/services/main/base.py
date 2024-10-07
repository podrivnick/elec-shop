from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass


@dataclass
class BaseCategoriesService(ABC):
    @abstractmethod
    def get_all_products_categories(self):
        raise NotImplementedError()


@dataclass
class BaseProductsService(ABC):
    @abstractmethod
    def get_filtered_products(self):
        raise NotImplementedError()

    @abstractmethod
    def paginate_products(self):
        raise NotImplementedError()
