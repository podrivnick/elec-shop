from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.api.v1.base_dto import BaseDTOAPI


@dataclass(frozen=True, eq=False)
class DTOPacketAPI(BaseDTOAPI):
    is_authenticated: bool = field(default=False)
    username: Optional[str] | None = field(default=None)
    product_id: Optional[int] | None = field(default=None)
    session_key: Optional[str] | None = field(default=None)
