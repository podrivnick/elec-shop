from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import (
    dataclass,
    field,
)
from typing import Iterable

from django.db.models import QuerySet

from core.apps.main.entities.product import ProductEntity
from core.apps.main.models.products import Products as ProductsModel


@dataclass
class BaseAllProductsService(ABC):
    products: Iterable[ProductEntity] = field(default=None, kw_only=True)

    @abstractmethod
    def get_all_products(self) -> QuerySet[ProductsModel]:
        raise NotImplementedError()


@dataclass
class BaseFavoriteProductsIdsService(ABC):
    @abstractmethod
    def get_ids_products_in_favorite(self):
        raise NotImplementedError()
