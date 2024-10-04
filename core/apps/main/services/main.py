from dataclasses import dataclass

from core.apps.main.services.base import (
    BaseCategoriesService,
    BaseFavoriteProductsIdsService,
    BaseProductsService,
)


@dataclass
class CategoriesService(BaseCategoriesService):
    def get_all_products_categories() -> None:
        print("s")


@dataclass
class FavoriteProductsIdsService(BaseFavoriteProductsIdsService):
    def get_favorite_products_ids() -> None:
        print("s")


@dataclass
class ProductsService(BaseProductsService):
    def get_filtered_products() -> None:
        print("s")
