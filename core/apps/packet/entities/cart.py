from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from typing import (
    Optional,
    Union,
)

from django.db.models import QuerySet

from core.apps.common.domain.base import ModelEntity
from core.apps.main.models.products import Products
from core.apps.users.models import User


@dataclass(frozen=True, eq=False)
class CartEntity(ModelEntity):
    user: QuerySet[User] | None = field(default=None)
    product: QuerySet[Products] | None = field(default=None)
    quantity: Optional[int] | None = field(default=None)
    session_key: Optional[str] | None = field(default=None)
    created_timestamp: Optional[Union[datetime, str]] = field(default=None)
