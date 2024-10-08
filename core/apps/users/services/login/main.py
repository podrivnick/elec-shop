from dataclasses import dataclass

from django.contrib import auth
from django.contrib.auth import authenticate
from django.http import HttpRequest

from core.apps.packet.models import Cart
from core.apps.users.entities.user import User as UserEntity
from core.apps.users.models import User
from core.apps.users.services.login.base import (
    BaseCommandAddPacketToUserBySessionKeyService,
    BaseCommandAuthenticateUserService,
    BaseCommandVerificateUserService,
)


@dataclass
class ORMCommandVerificateUserService(BaseCommandVerificateUserService):
    def verificate_password(
        self,
        request: HttpRequest,
        user: UserEntity,
    ) -> User:
        return authenticate(request, username=user.username, password=user.password)


@dataclass
class ORMCommandAuthenticateUserService(BaseCommandAuthenticateUserService):
    def login(
        self,
        user: User,
        request: HttpRequest,
    ) -> None:
        auth.login(request, user)


@dataclass
class ORMCommandAddPacketToUserBySessionKeyService(
    BaseCommandAddPacketToUserBySessionKeyService,
):
    def add_packet_to_user_by_session_key(
        self,
        user: User,
        session_key: str,
    ) -> None:
        Cart.objects.filter(session_key=session_key).update(user=user)
