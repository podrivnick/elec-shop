from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Iterable,
    List,
    Optional,
)

from core.api.v1.main.dto.base import BaseDTOAPI
from core.apps.main.entities.product import CategoriesProduct
from core.apps.main.schemas.main import PaginatedProductsResponse


@dataclass(frozen=True, eq=False)
class DTOResponseIndexAPI(BaseDTOAPI):
    favorites: List[int] | None = field(default_factory=list, kw_only=True)
    categories: Iterable[CategoriesProduct] | None = field(
        default_factory=list,
        kw_only=True,
    )
    is_search_failed: Optional[bool] | None = field(default=False)
    products: Optional[PaginatedProductsResponse] | None = field(default=None)
