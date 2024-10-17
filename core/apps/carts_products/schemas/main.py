from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Dict,
    Optional,
)

from core.apps.common.schemas.base import Schema


@dataclass(frozen=True, eq=False)
class ReviewDataSchema(Schema):
    id_product: Optional[str] | None = field(default=None)
    slug_product: Optional[str] | None = field(default=None)
    message: Optional[str] | None = field(default=None)

    def to_dict(self) -> Dict:
        return {
            "id_product": self.id_product,
            "slug_product": self.slug_product,
            "message": self.message,
        }
