from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass


@dataclass
class BaseQueryGetProductService(ABC):
    @abstractmethod
    def get_product_by_id(self):
        raise NotImplementedError()


@dataclass
class BaseQueryGetCartService(ABC):
    @abstractmethod
    def get_cart_by_product_and_user(self):
        raise NotImplementedError()


@dataclass
class BaseCommandUpdateDataCartService(ABC):
    @abstractmethod
    def update_or_create_cart(self):
        raise NotImplementedError()
