from functools import lru_cache

from punq import Container

from core.apps.main.services.favorites.favorites import (
    ORMFavoriteProductsIdsFilterService,
)
from core.apps.main.services.main.main import (
    ORMCategoriesService,
    ORMProductsService,
)
from core.apps.main.services.universal import (
    ORMAllProductsService,
    ORMFavoriteProductsIdsService,
)
from core.apps.main.use_cases.favorite import (
    FavoritePageCommand,
    FavoritePageCommandHandler,
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
    container.register(FavoritePageCommandHandler)

    def init_mediator() -> Mediator:
        mediator = Mediator()

        # command handlers
        configure_main_page_handler = MainPageCommandHandler(
            favorite_products_service_ids=ORMFavoriteProductsIdsService(),
            get_all_products_service=ORMAllProductsService(),
            categories_service=ORMCategoriesService(),
            products_service=ORMProductsService(),
        )

        configure_favorite_page_handler = FavoritePageCommandHandler(
            favorite_products_service_ids=ORMFavoriteProductsIdsService(),
            get_all_products_service=ORMAllProductsService(),
            products_service=ORMFavoriteProductsIdsFilterService(),
        )

        # commands
        mediator.register_command(
            MainPageCommand,
            [configure_main_page_handler],
        )

        mediator.register_command(
            FavoritePageCommand,
            [configure_favorite_page_handler],
        )

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
