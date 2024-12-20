from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.api.v1.base_dto import BaseDTOAPIUserData


@dataclass(frozen=True, eq=False)
class DTOCartPageAPI(BaseDTOAPIUserData):
    product_slug: Optional[str] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class DTOReviewPageAPI(BaseDTOAPIUserData):
    product_slug: Optional[str] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class DTOReviewCreateAPI(BaseDTOAPIUserData):
    review: Optional[str] | None = field(default=None)
    product_slug: Optional[str] | None = field(default=None)
    id_product: Optional[str] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class DTOReviewChangeAPI(BaseDTOAPIUserData):
    product_id: Optional[str] | None = field(default=None)
    review_id: Optional[str] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class DTOReviewDeleteAPI(BaseDTOAPIUserData):
    slug_product: Optional[str] | None = field(default=None)
    pk_product: Optional[str] | None = field(default=None)
