from dataclasses import (
    dataclass,
    field,
)

from core.api.v1.users.dto.responses import DTOResponseRegistrationAPI
from core.apps.common.exceptions.main import AuthenticationError
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
