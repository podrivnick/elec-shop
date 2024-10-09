from dataclasses import dataclass

from core.api.v1.main.dto.responses import DTOResponseInformationAPI
from core.apps.main.services.information.base import BaseQueryFAQInformationService
from core.infrastructure.mediator.base import BaseCommands
from core.infrastructure.mediator.handlers.commands import CommandHandler


@dataclass(frozen=True)
class InformationPageCommand(BaseCommands):
    pass


@dataclass(frozen=True)
class InformationPageCommandHandler(
    CommandHandler[InformationPageCommand, str],
):
    query_get_all_information: BaseQueryFAQInformationService

    def handle(
        self,
        command: InformationPageCommand,
    ) -> DTOResponseInformationAPI:
        all_info = self.query_get_all_information.get_all_information()

        return DTOResponseInformationAPI(
            info=all_info[0].text_info,
        )
