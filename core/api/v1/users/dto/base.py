from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Dict,
    Optional,
)

from django.utils.functional import SimpleLazyObject

from core.api.v1.base_dto import BaseDTOAPI
from core.apps.users.schemas.user_profile import ProfileDataSchema


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


@dataclass(frozen=True, eq=False)
class DTORegisterAPI(BaseDTOAPI):
    first_name: Optional[str] | None = field(default=None)
    last_name: Optional[str] | None = field(default=None)
    username: str | None = field(default=None)
    email: str | None = field(default=None)
    password1: str | None = field(default=None)
    password2: str | None = field(default=None)
    session_key: str | bool = field(default=False)
    is_authenticated: bool = field(default=False)


@dataclass(frozen=True, eq=False)
class DTOProiflePageAPI(BaseDTOAPI):
    user: SimpleLazyObject
    username: Optional[str] | None = field(default=None)
    referer: Optional[str] | None = field(default=None)
    is_authenticated: bool = field(default=False)
    updated_information: Optional[Dict] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class DTOProifleAPI(BaseDTOAPI):
    user: SimpleLazyObject
    username: Optional[str] | None = field(default=None)
    is_authenticated: bool = field(default=False)
    updated_data: Optional[ProfileDataSchema] | None = field(default=None)
    referer: Optional[str] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class DTOChangeTabAPI(BaseDTOAPI):
    is_authenticated: bool = field(default=False)
    is_packet: Optional[str] | None = field(default=None)
