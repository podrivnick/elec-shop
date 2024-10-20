from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from django.db.models import QuerySet

from core.apps.main.models.products import Products


@dataclass
class BaseQueryProductRepository(ABC):
    @abstractmethod
    def filter_product_by_slug(self) -> QuerySet[Products]:
        raise NotImplementedError()
