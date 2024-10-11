import logging
from dataclasses import dataclass

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from core.apps.users.entities.user import User as UserEntity
from core.apps.users.models import User
from core.apps.users.services.registration.base import (
    BaseCommandCreateUserService,
    BaseQueryUserInNotExistService,
)


@dataclass
class ORMQueryUserInNotExistService(BaseQueryUserInNotExistService):
    def verificate_user(
        self,
        user: UserEntity,
    ) -> QuerySet[User]:
        return get_user_model().objects.filter(username=user.username.to_raw()) or False


@dataclass
class ORMCommandCreateUserService(BaseCommandCreateUserService):
    @transaction.atomic
    def create_user(
        self,
        user: UserEntity,
    ) -> QuerySet[User]:
        logging.info(user)
        user_instance = get_user_model().objects.create(
            username=user.username.to_raw(),
            email=user.email.to_raw(),
            first_name=user.first_name.to_raw(),
            last_name=user.last_name.to_raw(),
        )
        user_instance.set_password(user.password.to_raw())
        user_instance.save()

        return user_instance
