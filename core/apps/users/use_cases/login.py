from dataclasses import (
    dataclass,
    field,
)

from django.http import HttpRequest

from core.api.v1.users.dto.responses import (
    DTOResponseAuthenticateAPI,
    DTOResponseLoginAPI,
)
from core.apps.common.exceptions.main import AuthenticationError
from core.apps.users import value_objects as vo
from core.apps.users.entities.user import User
from core.apps.users.exceptions.main import (
    UserNotAuthenticatedError,
    UserNotVerifiedError,
)
from core.apps.users.services.login.base import (
    BaseCommandAddPacketToUserBySessionKeyService,
    BaseCommandAuthenticateUserService,
    BaseCommandVerificateUserService,
)
from core.infrastructure.mediator.base import BaseCommands
from core.infrastructure.mediator.handlers.commands import CommandHandler


@dataclass(frozen=True)
class LoginPageCommand(BaseCommands):
    is_authenticated: bool = field(default=False)


@dataclass(frozen=True)
class LoginPageCommandHandler(CommandHandler[LoginPageCommand, str]):
    def handle(
        self,
        command: LoginPageCommand,
    ) -> DTOResponseLoginAPI:
        if command.is_authenticated:
            raise AuthenticationError("User is not authenticated.")

        return DTOResponseLoginAPI()


@dataclass(frozen=True)
class AuthenticatePageCommand(BaseCommands):
    username: str | None = field(default=None)
    email: str | None = field(default=None)
    password: str | None = field(default=None)
    session_key: str | None = field(default=None)
    is_authenticated: bool = field(default=False)
    request: HttpRequest | None = field(default=None)


@dataclass(frozen=True)
class AuthenticatePageCommandHandler(CommandHandler[AuthenticatePageCommand, str]):
    command_verificate_password_service: BaseCommandVerificateUserService
    command_authenticate_user_service: BaseCommandAuthenticateUserService
    command_add_packet_to_user_by_session_key: (
        BaseCommandAddPacketToUserBySessionKeyService
    )

    def handle(
        self,
        command: AuthenticatePageCommand,
    ) -> DTOResponseAuthenticateAPI:
        if command.is_authenticated:
            raise AuthenticationError("User is authenticated.")

        # value objects
        username = vo.UserName(command.username)
        password = vo.Password(command.password)

        # entity
        entity_user = User.create_user(
            username=username,
            password=password,
        )

        user = self.command_verificate_password_service.verificate_password(
            request=command.request,
            user=entity_user,
        )
        if user is None:
            raise UserNotVerifiedError(
                f"User '{entity_user.username.to_raw()}' not verified.",
            )

        try:
            self.command_authenticate_user_service.login(
                user=user,
                request=command.request,
            )
        except Exception:
            raise UserNotAuthenticatedError(
                f"{entity_user.username.to_raw()} not authenticated",
            )

        self.command_add_packet_to_user_by_session_key.add_packet_to_user_by_session_key(
            user=user,
            session_key=command.session_key,
        )

        return DTOResponseAuthenticateAPI(
            username=entity_user.username.to_raw(),
        )
