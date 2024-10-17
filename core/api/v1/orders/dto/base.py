from dataclasses import (
    dataclass,
    field,
)

from ninja import Query

from core.api.v1.base_dto import BaseDTOAPI
from core.api.v1.main.schemas import FiltersProductsSchema


@dataclass(frozen=True, eq=False)
class DTOMainPageAPI(BaseDTOAPI):
    filters: Query[FiltersProductsSchema]
    is_authenticated: bool = field(default=False)
    username: str | None = field(default=None)
    page_number: int = field(default=1)
    category_slug: str = field(default="all")
