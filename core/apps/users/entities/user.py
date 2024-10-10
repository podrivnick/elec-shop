from dataclasses import dataclass
from typing import Self

from core.apps.common.domain.base import Entity
from core.apps.users import value_objects as vo


@dataclass(frozen=True, eq=False)
class User(Entity):
    username: vo.UserName
    password: vo.Password

    @classmethod
    def create_user(
        cls,
        username: vo.UserName,
        password: vo.Password,
    ) -> Self:
        user = cls(
            username.to_raw(),
            password.to_raw(),
        )

        return user
