from functools import lru_cache

from punq import Container

from core.apps.main.services.main import (
    CategoriesService,
    FavoriteProductsIdsService,
    ORMProductsService,
)
from core.apps.main.use_cases.main import (
    MainPageCommand,
    MainPageCommandHandler,
)
from core.infrastructure.mediator.mediator import Mediator


@lru_cache(1)
def init_container() -> Container:
    return _initialize_container()


def _initialize_container() -> Container:
    container = Container()

    # Handlers
    container.register(MainPageCommandHandler)

    def init_mediator() -> Mediator:
        mediator = Mediator()

        # command handlers
        configure_main_page_handler = MainPageCommandHandler(
            categories_service=CategoriesService(),
            favorite_products_service_ids=FavoriteProductsIdsService(),
            products_service=ORMProductsService(),
        )

        # commands
        mediator.register_command(
            MainPageCommand,
            [configure_main_page_handler],
        )

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
