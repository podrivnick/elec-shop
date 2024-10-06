from dataclasses import (
    dataclass,
    field,
)
from typing import Dict

from core.api.filters import PaginationIn
from core.api.v1.main.schemas import FiltersProductsSchema
from core.apps.common.utils.context import convert_to_context_dict
from core.apps.main.services.base import (
    BaseCategoriesService,
    BaseFavoriteProductsIdsService,
    BaseProductsService,
)
from core.infrastructure.mediator.base import BaseCommands
from core.infrastructure.mediator.handlers.commands import CommandHandler


@dataclass(frozen=True)
class MainPageCommand(BaseCommands):
    is_authenticated: bool = field(default=False)
    username: str | None = field(default=None)
    filters: FiltersProductsSchema | None = field(default=None)
    pagination: PaginationIn | None = field(default=None)
    category_slug: str | None = field(default="all")


@dataclass(frozen=True)
class MainPageCommandHandler(CommandHandler[MainPageCommand, str]):
    categories_service: BaseCategoriesService
    favorite_products_service_ids: BaseFavoriteProductsIdsService
    products_service: BaseProductsService

    def handle(
        self,
        command: MainPageCommand,
    ) -> Dict:
        self.products_service.get_all_products()
        favorite_products_ids = None

        if command.is_authenticated:
            favorite_products_ids = (
                self.favorite_products_service_ids.get_ids_products_in_favorite(
                    command.username,
                )
            )
            # INFO: only ids of all products which mark as favorite

        categories = self.categories_service.get_all_products_categories()
        # INFO: just all categories of products

        is_search_failed, products = self.products_service.get_filtered_products(
            command.filters,
            command.pagination,
            command.category_slug,
        )  # INFO: should work even without filters

        context = convert_to_context_dict(
            favorite_products_ids=favorite_products_ids,
            categories=categories,
            is_search_failed=is_search_failed,
            products=products,
        )

        return context
