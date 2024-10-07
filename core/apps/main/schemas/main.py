from typing import List

from ninja import Schema

from core.apps.main.entities.product import (
    CategoriesProduct,
    ProductEntity,
)


class PaginatedProductsResponse(Schema):
    items: List[ProductEntity]
    current_page: int
    total_pages: int
    has_next: bool
    has_previous: bool


class BusinessDataResponseSchema(Schema):
    favorite_products_ids: List[int]
    categories: List[CategoriesProduct]
    is_search_failed: bool
    products: PaginatedProductsResponse
