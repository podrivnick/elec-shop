from dataclasses import dataclass

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from core.apps.common.services.base import BaseQueryGetUserModelService
from core.apps.users.models import User


@dataclass
class ORMQueryGetUserModelService(BaseQueryGetUserModelService):
    def get_usermodel_by_username(
        self,
        username: str,
    ) -> QuerySet[User]:
        return get_user_model().objects.get(username=username)
