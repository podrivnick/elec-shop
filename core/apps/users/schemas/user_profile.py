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
class ProfileDataSchema(Schema):
    first_name: Optional[str] | None = field(default=None)
    last_name: Optional[str] | None = field(default=None)
    username: Optional[str] | None = field(default=None)
    email: Optional[str] | None = field(default=None)
    phone: Optional[str] | None = field(default=None)
    image: Optional[str] | None = field(default=None)
    age: Optional[int] | None = field(default=0)

    def to_dict(self) -> Dict:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "image": self.image,
            "age": self.age,
        }
