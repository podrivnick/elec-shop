from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from typing import Optional

from core.apps.common.domain.base import ModelEntity
from core.apps.users.models import User


@dataclass(frozen=True, eq=False)
class ReviewEntity(ModelEntity):
    pk: int
    data_added: datetime
    user: User
    id_product: Optional[str] | None = field(default=None)
    review: Optional[str] | None = field(default=None)
    likes: Optional[int] | None = field(default=None)
