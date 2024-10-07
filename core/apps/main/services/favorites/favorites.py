from dataclasses import dataclass
from typing import List

from django.db.models import QuerySet

from core.apps.main.entities.product import ProductEntity
from core.apps.main.models.products import Products as ProductsModel
from core.apps.main.services.favorites.base import BaseFavoriteProductsIdsFilterService


@dataclass
class ORMFavoriteProductsIdsFilterService(BaseFavoriteProductsIdsFilterService):
    def get_filtered_products_by_favorite_ids(
        self,
        products: QuerySet[ProductsModel],
        ids_products_in_favorite: List[int],
    ) -> List[ProductEntity]:
        filter_products_by_favorite = products.filter(
            id_product__in=ids_products_in_favorite,
        )

        return [product.to_entity() for product in filter_products_by_favorite]
