from dataclasses import (
    dataclass,
    field,
)

from ninja import Query

from core.api.v1.main.schemas import FiltersProductsSchema


@dataclass(frozen=True, eq=False)
class BaseDTOAPI:
    pass


@dataclass(frozen=True, eq=False)
class DTOMainPageAPI(BaseDTOAPI):
    filters: Query[FiltersProductsSchema]
    is_authenticated: bool = field(default=False)
    username: str | None = field(default=None)
    page_number: int = field(default=1)
    category_slug: str = field(default="all")


@dataclass(frozen=True, eq=False)
class DTOFavoritePageAPI(BaseDTOAPI):
    username: str | None = field(default=None)
    is_authenticated: bool = field(default=False)
