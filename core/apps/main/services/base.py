from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass


@dataclass
class BaseCategoriesService(ABC):
    @abstractmethod
    def get_all_products_categories():
        raise NotImplementedError()


@dataclass
class BaseFavoriteProductsIdsService(ABC):
    @abstractmethod
    def get_favorite_products_ids():
        raise NotImplementedError()


@dataclass
class BaseProductsService(ABC):
    @abstractmethod
    def get_filtered_products():
        raise NotImplementedError()
