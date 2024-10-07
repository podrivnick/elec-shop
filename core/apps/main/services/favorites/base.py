from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass


@dataclass
class BaseFavoriteProductsIdsFilterService(ABC):
    @abstractmethod
    def get_filtered_products_by_favorite_ids(self):
        raise NotImplementedError()
