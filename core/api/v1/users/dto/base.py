from dataclasses import (
    dataclass,
    field,
)

from core.api.v1.base_dto import BaseDTOAPI


@dataclass(frozen=True, eq=False)
class DTOLoginPageAPI(BaseDTOAPI):
    username: str | None = field(default=None)
    is_authenticated: bool = field(default=False)
