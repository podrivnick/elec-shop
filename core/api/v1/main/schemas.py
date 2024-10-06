from typing import Optional

from ninja import Schema


class FiltersProductsSchema(Schema):
    available: Optional[str] = None
    discount: Optional[str] = None
    sorting: Optional[str] = "default"
    search: Optional[str] = None


class ProductIdSchema(Schema):
    product_id: str
