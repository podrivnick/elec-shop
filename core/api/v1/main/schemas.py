from typing import Optional

from ninja import Schema


class FiltersProductsSchema(Schema):
    is_available: Optional[bool] = None
    is_discount: Optional[bool] = None
    is_sorting: Optional[bool] = None
    query: Optional[str] = None
    # category_slug: Optional[str] = "all"


class ProductIdSchema(Schema):
    product_id: str
