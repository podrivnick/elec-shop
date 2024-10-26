from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.api.v1.base_dto import BaseDTOAPIUserData


@dataclass(frozen=True, eq=False)
class DTOCreateOrderAPI(BaseDTOAPIUserData):
    is_authenticated: bool = field(default=False)
    username: Optional[str] | None = field(default=None)
    first_name: Optional[str] | None = field(default=None)
    last_name: Optional[str] | None = field(default=None)
    email: Optional[str] | None = field(default=None)
    phone: Optional[str] | None = field(default=None)
    delivery_address: Optional[str] | None = field(default=None)
    required_delivery: Optional[str] | None = field(default=None)
    payment_on_get: Optional[str] | None = field(default=None)
    total_price: Optional[str] | None = field(default=None)
