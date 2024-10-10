from dataclasses import dataclass

from django.contrib.auth import logout
from django.http import HttpRequest

from core.apps.users.services.logout.base import BaseCommandLogoutUserService


@dataclass
class ORMCommandLogoutUserService(BaseCommandLogoutUserService):
    def logout_user(
        self,
        request: HttpRequest,
    ) -> None:
        return logout(request)
