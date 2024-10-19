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
