from dataclasses import (
    dataclass,
    field,
)
from typing import (
    List,
    Optional,
)

from core.api.v1.main.dto.base import BaseDTOAPI
from core.apps.packet.entities.cart import CartEntity
from core.apps.users.schemas.user_profile import ProfileDataSchema


@dataclass(frozen=True, eq=False)
class DTOResponseLoginAPI(BaseDTOAPI):
    username: Optional[str] | None = field(default=None)
    email: Optional[str] | None = field(default=None)
    password: Optional[str] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class DTOResponseAuthenticateAPI(BaseDTOAPI):
    username: str | None = field(default=None)
    email: str | None = field(default=None)
    password: str | None = field(default=None)
    session_key: str | bool = field(default=False)
    is_authenticated: bool = field(default=False)


@dataclass(frozen=True, eq=False)
class DTOResponseLogoutPageAPI(BaseDTOAPI):
    username: str | None = field(default=None)
    is_authenticated: bool = field(default=False)


@dataclass(frozen=True, eq=False)
class DTOResponseRegistrationAPI(BaseDTOAPI):
    first_name: Optional[str] | None = field(default=None)
    last_name: Optional[str] | None = field(default=None)
    username: Optional[str] | None = field(default=None)
    email: Optional[str] | None = field(default=None)
    password1: Optional[str] | None = field(default=None)
    password2: Optional[str] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class DTOResponseRegisterAPI(BaseDTOAPI):
    username: Optional[str] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class DTOResponseProfileAPI(BaseDTOAPI):
    form: ProfileDataSchema | None = field(default=None)
    is_packet: Optional[bool] = field(default=True)
    packet: List[CartEntity] | None = field(default=None)
    referer: Optional[str] | None = field(default=None)
