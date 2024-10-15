from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.api.v1.base_dto import BaseDTOAPI


@dataclass(frozen=True, eq=False)
class DTOBasePacket(BaseDTOAPI):
    is_authenticated: bool = field(default=False)
    username: Optional[str] | None = field(default=None)
    session_key: Optional[str] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class DTOPacketAPI(DTOBasePacket):
    product_id: Optional[int] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class DTODeletePacketAPI(DTOBasePacket):
    cart_id: Optional[int] | None = field(default=None)
    is_profile: Optional[str] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class DTOChangePacketAPI(DTOBasePacket):
    is_plus: Optional[int] | None = field(default=None)
    cart_id: Optional[int] | None = field(default=None)
    is_profile: Optional[str] | None = field(default=None)
