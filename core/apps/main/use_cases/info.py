from dataclasses import (
    dataclass,
    field,
)

from src.domain.flowers.entities.flower import (
    BaseFAQInformationService,
    Flower,
)

from core.infrastructure.mediator.base import BaseCommands
from core.infrastructure.mediator.handlers.commands import CommandHandler


@dataclass(frozen=True)
class InformationPageCommand(BaseCommands):
    flower: str | None = field(default=None)


@dataclass(frozen=True)
class InformationPageCommandHandler(CommandHandler[InformationPageCommand, Flower]):
    information: BaseFAQInformationService

    def handle(
        self,
        command: InformationPageCommand,
    ) -> Flower:
        all_info = (
            self.information.get_all_information()
        )  # INFO: just return all information

        return all_info
