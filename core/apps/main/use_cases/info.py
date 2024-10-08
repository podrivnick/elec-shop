from dataclasses import dataclass
from typing import (
    Dict,
    List,
)

from core.apps.common.utils.context import convert_to_context_dict
from core.apps.main.entities.information import InformationEntity
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
    ) -> Dict[str, List[InformationEntity]]:
        all_info = self.query_get_all_information.get_all_information()

        context = convert_to_context_dict(
            info=all_info[0].text_info,
        )

        return context
