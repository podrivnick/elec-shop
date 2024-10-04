from dataclasses import (
    dataclass,
    field,
)

from core.infrastructure.mediator.base import BaseCommands
from core.infrastructure.mediator.handlers.commands import CommandHandler


class BaseFAQInformationService:
    pass


@dataclass(frozen=True)
class InformationPageCommand(BaseCommands):
    flower: str | None = field(default=None)


@dataclass(frozen=True)
class InformationPageCommandHandler(CommandHandler[InformationPageCommand, str]):
    information: BaseFAQInformationService

    def handle(
        self,
        command: InformationPageCommand,
    ) -> str:
        all_info = (
            self.information.get_all_information()
        )  # INFO: just return all information

        return all_info
