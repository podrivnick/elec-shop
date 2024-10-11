from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from django.http import HttpRequest

from core.api.v1.users.dto.responses import (
    DTOResponseRegisterAPI,
    DTOResponseRegistrationAPI,
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
)
from core.apps.users.services.registration.base import (
    BaseCommandCreateUserService,
    BaseQueryUserInNotExistService,
)
from core.infrastructure.mediator.base import BaseCommands
from core.infrastructure.mediator.handlers.commands import CommandHandler


@dataclass(frozen=True)
class RegistrationPageCommand(BaseCommands):
    is_authenticated: bool = field(default=False)


@dataclass(frozen=True)
class RegistrationPageCommandHandler(CommandHandler[RegistrationPageCommand, str]):
    def handle(
        self,
        command: RegistrationPageCommand,
    ) -> DTOResponseRegistrationAPI:
        if command.is_authenticated:
            raise AuthenticationError("User is authenticated.")

        return DTOResponseRegistrationAPI()


@dataclass(frozen=True)
class RegisterCommand(BaseCommands):
    first_name: Optional[str] | None = field(default=None)
    last_name: Optional[str] | None = field(default=None)
    username: str | None = field(default=None)
    email: str | None = field(default=None)
    password1: str | None = field(default=None)
    password2: str | None = field(default=None)
    session_key: str | bool = field(default=False)
    is_authenticated: bool = field(default=False)
    request: HttpRequest | None = field(default=None)


@dataclass(frozen=True)
class RegisterCommandHandler(CommandHandler[RegisterCommand, str]):
    query_verificate_user_is_not_exist: BaseQueryUserInNotExistService
    command_create_user_by_enter_data: BaseCommandCreateUserService
    command_authenticate_user_service: BaseCommandAuthenticateUserService
    command_add_packet_to_user_by_session_key: (
        BaseCommandAddPacketToUserBySessionKeyService
    )

    def handle(
        self,
        command: RegisterCommand,
    ) -> DTOResponseRegisterAPI:
        if command.is_authenticated:
            raise AuthenticationError("User is authenticated.")

        # value objects
        username = vo.UserName(command.username)
        first_name = vo.FirstName(command.first_name)
        last_name = vo.LastName(command.last_name)
        email = vo.Email(command.email)
        password1 = vo.Password(command.password1)
        password2 = vo.Password(command.password2)

        # entity
        entity_user = User.create_user(
            username=username,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password2=password2,
        )

        user = self.query_verificate_user_is_not_exist.verificate_user(user=entity_user)
        if user:
            raise UserNotVerifiedError("User Verified")

        try:
            user_model = self.command_create_user_by_enter_data.create_user(
                user=entity_user,
            )
        except Exception:
            raise ValueError("Some Error Server")

        try:
            self.command_authenticate_user_service.login(
                user=user_model,
                request=command.request,
            )
        except Exception:
            raise UserNotAuthenticatedError(
                f"{entity_user.username.to_raw()} not authenticated",
            )

        try:
            self.command_add_packet_to_user_by_session_key.add_packet_to_user_by_session_key(
                user=user_model,
                session_key=command.session_key,
            )
        except Exception:
            raise ValueError("Some Error In Server")

        return DTOResponseRegisterAPI(
            username=entity_user.username.to_raw(),
        )
