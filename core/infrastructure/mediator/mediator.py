from collections import defaultdict
from collections.abc import Iterable
from dataclasses import (
    dataclass,
    field,
)

from core.infrastructure.mediator.base import BaseCommands
from core.infrastructure.mediator.handlers.commands import (
    CommandHandler,
    CR,
    CT,
)
from core.infrastructure.mediator.sub_mediators.commands import CommandMediator


# TODO: create CommandHandlerNotRegisteredException()
@dataclass(eq=False)
class Mediator(CommandMediator):
    commands_map: dict[CR, CommandHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    def register_command(
        self,
        command: CT,
        command_handlers: Iterable[CommandHandler[CT, CR]],
    ) -> None:
        self.commands_map[command].extend(command_handlers)

    def handle_command(self, command: BaseCommands) -> Iterable[CR]:
        event_type = command.__class__
        handlers = self.commands_map.get(event_type)

        if not handlers:
            raise ValueError()

        return [handler.handle(command) for handler in handlers]
