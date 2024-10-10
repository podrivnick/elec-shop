from dataclasses import (
    dataclass,
    field,
)

from core.api.v1.base_dto import BaseDTOAPI


@dataclass(frozen=True, eq=False)
class DTOLoginPageAPI(BaseDTOAPI):
    username: str | None = field(default=None)
    is_authenticated: bool = field(default=False)


@dataclass(frozen=True, eq=False)
class DTORegistrationPageAPI(BaseDTOAPI):
    username: str | None = field(default=None)
    is_authenticated: bool = field(default=False)


@dataclass(frozen=True, eq=False)
class DTOAuthenticateAPI(BaseDTOAPI):
    username: str | None = field(default=None)
    email: str | None = field(default=None)
    password: str | None = field(default=None)
    session_key: str | bool = field(default=False)
    is_authenticated: bool = field(default=False)


@dataclass(frozen=True, eq=False)
class DTOLogoutPageAPI(BaseDTOAPI):
    username: str | None = field(default=None)
    is_authenticated: bool = field(default=False)
