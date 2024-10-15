from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.api.v1.main.dto.base import BaseDTOAPI


@dataclass(frozen=True, eq=False)
class DTOResponseAddPacketAPI(BaseDTOAPI):
    carts_items_user: Optional[str] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class DTOResponseDeletePacketAPI(BaseDTOAPI):
    carts_items_user: Optional[str] | None = field(default=None)
    new_quantity: Optional[int] | None = field(default=None)
