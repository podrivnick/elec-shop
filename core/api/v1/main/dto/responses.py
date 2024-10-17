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
from core.apps.main.entities.information import InformationEntity
from core.apps.main.entities.product import (
    CategoriesProduct,
    ProductEntity,
)
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


@dataclass(frozen=True, eq=False)
class DTOResponseFavoriteAPI(BaseDTOAPI):
    products: List[ProductEntity] | None = field(default_factory=list, kw_only=True)


@dataclass(frozen=True, eq=False)
class DTOResponseInformationAPI(BaseDTOAPI):
    info: List[InformationEntity] | None = field(default_factory=list, kw_only=True)
