from functools import lru_cache

from punq import Container
from src.application.arts.commands.arts import (
    GetRandomArtCommand,
    GetRandomArtCommandHandler,
)
from src.infrastructure.db.services import BaseArtMongoDBService
from src.infrastructure.mediator.main import Mediator


@lru_cache(1)
def init_container() -> Container:
    return _initialize_container()


def _initialize_container() -> Container:
    container = Container()

    # Handlers
    container.register(GetRandomArtCommandHandler)

    def init_mediator() -> Mediator:
        mediator = Mediator()

        # command handlers
        get_random_art_handler = GetRandomArtCommandHandler(
            arts_service=container.resolve(BaseArtMongoDBService),
        )

        # commands
        mediator.register_command(
            GetRandomArtCommand,
            [get_random_art_handler],
        )

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
