from dataclasses import dataclass
from typing import (
    Iterable,
    List,
)

from core.api.filters import PaginationIn
from core.api.v1.main.schemas import FiltersProductsSchema
from core.apps.main.entities.product import (
    CategoriesProduct,
    ProductEntity,
)
from core.apps.main.models.favorites import Favorites
from core.apps.main.models.products import (
    CategoriesProduct as CategoriesProductModel,
    Products as ProductsModel,
)
from core.apps.main.services.base import (
    BaseCategoriesService,
    BaseFavoriteProductsIdsService,
    BaseProductsService,
)
from core.apps.main.utils.main import q_search


@dataclass
class CategoriesService(BaseCategoriesService):
    def get_all_products_categories(self) -> Iterable[CategoriesProduct]:
        categories = CategoriesProductModel.objects.all()

        return [category.to_entity() for category in categories]


@dataclass
class FavoriteProductsIdsService(BaseFavoriteProductsIdsService):
    def get_ids_products_in_favorite(self, username: str) -> List:
        favorites = Favorites.objects.filter(user__username=username)
        products_id = [item.product_id for item in favorites]

        return products_id


@dataclass
class ProductsService(BaseProductsService):
    def get_all_products(self) -> None:
        self.products = ProductsModel.objects.all()

    def get_filtered_products(
        self,
        filters: FiltersProductsSchema,
        pagination: PaginationIn,
        category_slug: str,
    ) -> tuple[bool, Iterable[ProductEntity]]:
        is_search_failed = False

        if filters.is_available:
            self.products = self.products.filter(count_product__gt=0)

        if filters.is_discount:
            self.products = self.products.filter(discount__gt=0)

        if filters.is_sorting and filters.is_sorting != "default":
            self.products = self.products.order_by(filters.is_sorting)

        if category_slug and category_slug != "all":
            self.products = self.products.filter(category__slug=category_slug)

        if filters.query:
            self.products = q_search(filters.query, self.products)

            if not len(self.products):
                is_search_failed = True

        self.products = self.products.filter()[
            pagination.offset : pagination.offset + pagination.limit
        ]

        return is_search_failed, [product.to_entity() for product in self.products]
