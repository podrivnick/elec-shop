from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from core.apps.main.entities.product import ProductEntity


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

    @abstractmethod
    def get_filtered_product_by_slug(self) -> ProductEntity:
        raise NotImplementedError()
