from dataclasses import dataclass
from typing import (
    Iterable,
    List,
    QuerySet,
    Tuple,
)

from django.core.paginator import Paginator

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
from core.apps.main.schemas.main import PaginatedProductsResponse
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
class ORMProductsService(BaseProductsService):
    def get_all_products(self) -> QuerySet[ProductsModel]:
        self.products = ProductsModel.objects.all()

    def get_filtered_products(
        self,
        filters: FiltersProductsSchema,
        category_slug: str,
    ) -> Tuple[bool, Iterable[ProductEntity]]:
        """Filtering Products + Search."""

        is_search_failed = False

        if filters.available:
            self.products = self.products.filter(count_product__gt=0)

        if filters.discount:
            self.products = self.products.filter(discount__gt=0)

        if filters.sorting and filters.sorting != "default":
            self.products = self.products.order_by(filters.sorting)

        if category_slug and category_slug != "all":
            self.products = self.products.filter(category__slug=category_slug)

        if filters.search:
            self.products = q_search(filters.search, self.products)

            if not len(self.products):
                is_search_failed = True

        return is_search_failed, [product.to_entity() for product in self.products]

    def paginate_products(
        self,
        page_number: int,
        products: List[ProductEntity],
    ) -> PaginatedProductsResponse:
        """Convert Product to Paginator."""

        paginator = Paginator(products, 6)
        page_obj = paginator.get_page(page_number)

        paginated_response = PaginatedProductsResponse(
            items=page_obj.object_list,
            current_page=page_obj.number,
            total_pages=paginator.num_pages,
            has_next=page_obj.has_next(),
            has_previous=page_obj.has_previous(),
        )

        return paginated_response
