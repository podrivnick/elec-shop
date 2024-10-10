from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from django.http import HttpRequest

from core.api.v1.users.dto.responses import DTOResponseLogoutPageAPI
from core.apps.common.exceptions.main import (
    AuthenticationError,
    LogoutUserError,
)
from core.apps.users.services.logout.base import BaseCommandLogoutUserService
from core.infrastructure.mediator.base import BaseCommands
from core.infrastructure.mediator.handlers.commands import CommandHandler


@dataclass(frozen=True)
class LogoutCommand(BaseCommands):
    username: Optional[str] | None = field(default=None)
    is_authenticated: Optional[bool] | None = field(default=False)
    request: HttpRequest | None = field(default=None)


@dataclass(frozen=True)
class LogoutCommandHandler(CommandHandler[LogoutCommand, str]):
    command_logout_user_service: BaseCommandLogoutUserService

    def handle(
        self,
        command: LogoutCommand,
    ) -> DTOResponseLogoutPageAPI:
        if not command.is_authenticated:
            raise AuthenticationError("User is not authenticated.")

        try:
            self.command_logout_user_service.logout_user(
                request=command.request,
            )
        except Exception:
            raise LogoutUserError(f"User {command.username} not logouted")

        return DTOResponseLogoutPageAPI(
            username=command.username,
        )
