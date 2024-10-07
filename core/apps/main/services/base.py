from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import (
    dataclass,
    field,
)
from typing import Iterable

from core.apps.main.entities.product import ProductEntity


@dataclass
class BaseCategoriesService(ABC):
    @abstractmethod
    def get_all_products_categories(self):
        raise NotImplementedError()


@dataclass
class BaseFavoriteProductsIdsService(ABC):
    @abstractmethod
    def get_ids_products_in_favorite(self):
        raise NotImplementedError()


@dataclass
class BaseProductsService(ABC):
    products: Iterable[ProductEntity] = field(default=None, kw_only=True)

    @abstractmethod
    def get_filtered_products(self):
        raise NotImplementedError()

    @abstractmethod
    def get_all_products(self):
        raise NotImplementedError()

    @abstractmethod
    def paginate_products(self):
        raise NotImplementedError()
