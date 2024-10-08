from typing import (
    List,
    Optional,
)

from ninja import Schema

from core.apps.main.entities.product import (
    CategoriesProduct,
    ProductEntity,
)


class PaginatedProductsResponse(Schema):
    items: List[ProductEntity]
    current_page: Optional[int]
    total_pages: Optional[int]
    has_next: Optional[bool]
    has_previous: Optional[bool]


class BusinessDataResponseSchema(Schema):
    favorite_products_ids: List[int]
    categories: List[CategoriesProduct]
    is_search_failed: Optional[bool]
    products: PaginatedProductsResponse
