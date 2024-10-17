from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.api.v1.base_dto import BaseDTOAPI


@dataclass(frozen=True, eq=False)
class DTOCartPageAPI(BaseDTOAPI):
    is_authenticated: bool = field(default=False)
    username: str | None = field(default=None)
    product_slug: Optional[str] | None = field(default=None)
