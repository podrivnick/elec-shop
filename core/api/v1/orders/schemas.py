from typing import Optional

from ninja import Schema

from core.apps.main.schemas.main import BusinessDataResponseSchema


class FiltersProductsSchema(Schema):
    available: Optional[str] = None
    discount: Optional[str] = None
    sorting: Optional[str] = "default"
    search: Optional[str] = None


class MainPageResponseSchema(Schema):
    context: BusinessDataResponseSchema


class ProductIdSchema(Schema):
    product_id: str
