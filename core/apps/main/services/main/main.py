from dataclasses import dataclass
from typing import (
    Iterable,
    List,
    Optional,
    Tuple,
)

from django.core.paginator import Paginator
from django.db.models import QuerySet

from core.api.v1.main.schemas import FiltersProductsSchema
from core.apps.main.entities.product import (
    CategoriesProduct,
    ProductEntity,
)
from core.apps.main.models.products import (
    CategoriesProduct as CategoriesProductModel,
    Products as ProductsModel,
)
from core.apps.main.repositories.base import BaseQueryProductRepository
from core.apps.main.schemas.main import PaginatedProductsResponse
from core.apps.main.services.main.base import (
    BaseCategoriesService,
    BaseProductsService,
)
from core.apps.main.utils.main import q_search


@dataclass
class ORMCategoriesService(BaseCategoriesService):
    def get_all_products_categories(self) -> Iterable[CategoriesProduct]:
        categories = CategoriesProductModel.objects.all()

        return [category.to_entity() for category in categories]


@dataclass
class ORMProductsService(BaseProductsService):
    query_product_repository: BaseQueryProductRepository

    def get_filtered_products(
        self,
        products: QuerySet[ProductsModel],
        filters: FiltersProductsSchema,
        category_slug: str,
    ) -> Tuple[bool, Iterable[ProductEntity]]:
        """Filtering Products + Search."""
        # TODO: fix architecture
        is_search_failed = False

        if filters.available:
            products = products.filter(count_product__gt=0)

        if filters.discount:
            products = products.filter(discount__gt=0)

        if filters.sorting and filters.sorting != "default":
            products = products.order_by(filters.sorting)

        if category_slug and category_slug != "all":
            products = products.filter(category__slug=category_slug)

        if filters.search:
            products = q_search(filters.search, products)

            if not len(products):
                is_search_failed = True

        return is_search_failed, [product.to_entity() for product in products]

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

    def get_filtered_product_by_slug(
        self,
        slug: Optional[str],
    ) -> ProductEntity:
        product = self.query_product_repository.filter_product_by_slug(slug=slug)

        return [item.to_entity() for item in product][0]
