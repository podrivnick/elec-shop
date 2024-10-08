from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass


@dataclass
class BaseQueryUpdateFavoriteProductsService(ABC):
    @abstractmethod
    def check_product_in_favorite_is_exist(self):
        raise NotImplementedError()


@dataclass
class BaseCommandUpdateFavoriteProductsService(ABC):
    @abstractmethod
    def add_product_to_favorite(self):
        raise NotImplementedError()

    @abstractmethod
    def delete_product_from_favorite(self):
        raise NotImplementedError()
