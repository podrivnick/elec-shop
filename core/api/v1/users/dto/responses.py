from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.api.v1.main.dto.base import BaseDTOAPI


@dataclass(frozen=True, eq=False)
class DTOResponseLoginAPI(BaseDTOAPI):
    username: Optional[str] | None = field(default=None)
    email: Optional[str] | None = field(default=None)
    password: Optional[str] | None = field(default=None)
