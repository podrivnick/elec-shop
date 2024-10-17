from dataclasses import (
    dataclass,
    field,
)
from typing import (
    List,
    Optional,
)

from core.api.v1.main.dto.base import BaseDTOAPI
from core.apps.main.entities.product import ProductEntity


LikesEntity = 1
ReviewEntity = 4
ReviewForomSchema = 4


@dataclass(frozen=True, eq=False)
class DTOResponseCartAPI(BaseDTOAPI):
    products: ProductEntity | None = field(default=None)
    favorites: List[int] | None = field(default_factory=list, kw_only=True)
    count_all_opinions: Optional[int] | None = field(default=None)
    liked_objects: List[LikesEntity] | None = field(default=None)
    opinions: List[ReviewEntity] | None = field(default=None)
    form: ReviewForomSchema | None = field(default=None)
