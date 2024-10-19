from dataclasses import (
    dataclass,
    field,
)


@dataclass(frozen=True, eq=False)
class BaseDTOAPI:
    pass


@dataclass(frozen=True, eq=False)
class BaseDTOAPIUserData(BaseDTOAPI):
    is_authenticated: bool = field(default=False)
    username: str | None = field(default=None)
