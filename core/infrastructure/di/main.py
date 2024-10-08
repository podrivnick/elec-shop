from functools import lru_cache
from core.apps.main.use_cases.update_favorite import (
    UpdateFavoritePageCommand,
    UpdateFavoritePageCommandHandler,
)
from core.apps.main.use_cases.info import (
    InformationPageCommand,
    InformationPageCommandHandler,
)
from punq import Container
from core.apps.common.services.main import ORMQueryGetUserModelService
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
from core.apps.main.services.information.main import ORMQueryFAQInformationService
from core.infrastructure.mediator.mediator import Mediator
from core.apps.main.services.update_favorite.main import (
    ORMCommandUpdateFavoriteProductsService,
    ORMQueryUpdateFavoriteProductsService,
)


@lru_cache(1)
def init_container() -> Container:
    return _initialize_container()


def _initialize_container() -> Container:
    container = Container()

    # Handlers
    container.register(MainPageCommandHandler)
    container.register(FavoritePageCommandHandler)
    container.register(UpdateFavoritePageCommandHandler)
    container.register(InformationPageCommandHandler)

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

        configure_update_favorite_products_handler = UpdateFavoritePageCommandHandler(
            query_get_user_model_by_username=ORMQueryGetUserModelService(),
            query_update_favorite_product_service=ORMQueryUpdateFavoriteProductsService(),
            command_update_favorite_product_service=ORMCommandUpdateFavoriteProductsService(),
        )

        configure_information_page_handler = InformationPageCommandHandler(
            query_get_all_information=ORMQueryFAQInformationService(),
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

        mediator.register_command(
            UpdateFavoritePageCommand,
            [configure_update_favorite_products_handler],
        )

        mediator.register_command(
            InformationPageCommand,
            [configure_information_page_handler],
        )

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
