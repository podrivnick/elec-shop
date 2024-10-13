from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Dict,
    Self,
)

from core.apps.common.domain.base import Entity
from core.apps.users import value_objects as vo
from core.apps.users.exceptions.main import UserPasswordsIsNotEqual


@dataclass(frozen=True, eq=False)
class User(Entity):
    username: vo.UserName | None = field(default=None)
    password: vo.Password | None = field(default=None)
    first_name: vo.FirstName | None = field(default=None)
    last_name: vo.LastName | None = field(default=None)
    email: vo.Email | None = field(default=None)
    password2: vo.Password | None = field(default=None)
    phone: vo.PhoneNumber | None = field(default=None)
    image: vo.ImageUser | None = field(default=None)
    age: vo.AgeUser | None = field(default=None)

    @classmethod
    def create_user(
        cls,
        username: vo.UserName = None,
        password: vo.Password = None,
        first_name: vo.FirstName = None,
        last_name: vo.LastName = None,
        email: vo.Email = None,
        password2: vo.Password = None,
        age: vo.AgeUser = None,
        phone: vo.PhoneNumber = None,
        image: vo.ImageUser = None,
    ) -> Self:
        if password2 is not None and password != password2:
            raise UserPasswordsIsNotEqual("Password is Not Equal")

        user = cls(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            age=age,
            phone=phone,
            image=image,
        )

        return user

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
