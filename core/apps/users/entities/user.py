from dataclasses import (
    dataclass,
    field,
)
from typing import Self

from core.apps.common.domain.base import Entity
from core.apps.users import value_objects as vo
from core.apps.users.exceptions.main import UserPasswordsIsNotEqual


@dataclass(frozen=True, eq=False)
class User(Entity):
    username: vo.UserName
    password: vo.Password
    first_name: vo.FirstName | None = field(default=None)
    last_name: vo.LastName | None = field(default=None)
    email: vo.Email | None = field(default=None)
    password2: vo.Password | None = field(default=None)

    @classmethod
    def create_user(
        cls,
        username: vo.UserName,
        password: vo.Password,
        first_name: vo.FirstName = None,
        last_name: vo.LastName = None,
        email: vo.Email = None,
        password2: vo.Password = None,
    ) -> Self:
        if password2 is not None and password != password2:
            raise UserPasswordsIsNotEqual("Password is Not Equal")

        user = cls(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        return user
