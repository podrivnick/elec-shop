from dataclasses import (
    dataclass,
    field,
)

from core.api.v1.main.dto.responses import DTOResponseIndexAPI
from core.api.v1.main.schemas import FiltersProductsSchema
from core.apps.main.services.base import (
    BaseAllProductsService,
    BaseFavoriteProductsIdsService,
)
from core.apps.main.services.main.base import (
    BaseCategoriesService,
    BaseProductsService,
)
from core.infrastructure.mediator.base import BaseCommands
from core.infrastructure.mediator.handlers.commands import CommandHandler


@dataclass(frozen=True)
class MainPageCommand(BaseCommands):
    is_authenticated: bool = field(default=False)
    username: str | None = field(default=None)
    filters: FiltersProductsSchema | None = field(default=None)
    page_number: int | None = field(default=None)
    category_slug: str | None = field(default="all")


@dataclass(frozen=True)
class MainPageCommandHandler(CommandHandler[MainPageCommand, str]):
    favorite_products_service_ids: BaseFavoriteProductsIdsService
    get_all_products_service: BaseAllProductsService
    categories_service: BaseCategoriesService
    products_service: BaseProductsService

    def handle(
        self,
        command: MainPageCommand,
    ) -> DTOResponseIndexAPI:
        products = self.get_all_products_service.get_all_products()

        if not command.is_authenticated:
            favorite_products_ids = None

        favorite_products_ids = (
            self.favorite_products_service_ids.get_ids_products_in_favorite(
                command.username,
            )
        )

        categories = self.categories_service.get_all_products_categories()

        is_search_failed, products = self.products_service.get_filtered_products(
            products=products,
            filters=command.filters,
            category_slug=command.category_slug,
        )

        paginated_response = self.products_service.paginate_products(
            page_number=command.page_number,
            products=products,
        )

        return DTOResponseIndexAPI(
            favorites=favorite_products_ids,
            categories=categories,
            is_search_failed=is_search_failed,
            products=paginated_response,
        )
