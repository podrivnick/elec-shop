from dataclasses import dataclass
from typing import List

from django.db.models import QuerySet

from core.apps.main.models.favorites import Favorites
from core.apps.main.models.products import Products as ProductsModel
from core.apps.main.services.base import (
    BaseAllProductsService,
    BaseFavoriteProductsIdsService,
)


@dataclass
class ORMAllProductsService(BaseAllProductsService):
    def get_all_products(self) -> QuerySet[ProductsModel]:
        self.products = ProductsModel.objects.all()
        return self.products


@dataclass
class ORMFavoriteProductsIdsService(BaseFavoriteProductsIdsService):
    def get_ids_products_in_favorite(self, username: str) -> List[int]:
        favorites = Favorites.objects.filter(user__username=username)
        products_id = [item.product_id for item in favorites]

        return products_id
