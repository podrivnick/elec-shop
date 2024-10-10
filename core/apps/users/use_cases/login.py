from dataclasses import (
    dataclass,
    field,
)

from core.api.v1.users.dto.responses import DTOResponseLoginAPI
from core.apps.common.exceptions.main import AuthenticationError
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
