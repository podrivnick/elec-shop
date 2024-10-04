from dataclasses import dataclass
from typing import Iterable

from core.api.filters import PaginationIn
from core.api.v1.main.schemas import FiltersProductsSchema
from core.apps.main.entities.product import ProductEntity
from core.apps.main.models.products import Products as ProductsModel
from core.apps.main.services.base import (
    BaseCategoriesService,
    BaseFavoriteProductsIdsService,
    BaseProductsService,
)
from core.apps.main.utils.main import q_search


@dataclass
class CategoriesService(BaseCategoriesService):
    def get_all_products_categories(self) -> None:
        print("s")


@dataclass
class FavoriteProductsIdsService(BaseFavoriteProductsIdsService):
    def get_favorite_products_ids(self) -> None:
        print("s")


@dataclass
class ProductsService(BaseProductsService):
    def get_all_products(self) -> None:
        self.products = ProductsModel.object.all()

    def get_filtered_products(
        self,
        filters: FiltersProductsSchema,
        pagination: PaginationIn,
    ) -> tuple[bool, Iterable[ProductEntity]]:
        is_search_failed = False

        if self.is_available:
            self.products = self.products.filter(count_product__gt=0)

        if self.is_discount:
            self.products = self.products.filter(discount__gt=0)

        if self.is_sorting and self.is_sorting != "default":
            self.products = self.products.order_by(self.is_sorting)

        if self.slug and self.slug != "all":
            self.products = self.products.filter(category__slug=self.slug)

        if self.query:
            self.products = q_search(self.query, self.products)

            if not len(self.products):
                is_search_failed = True

        self.products = self.products.filter()[
            pagination.offset : pagination.offset + pagination.limit
        ]

        return is_search_failed, [product.to_entity() for product in self.products]
