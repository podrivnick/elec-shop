from dataclasses import (
    dataclass,
    field,
)

from src.domain.flowers.entities.flower import (
    BaseCategoriesService,
    BaseFavoriteProductsIdsService,
    BaseProductsService,
    Flower,
)

from core.infrastructure.mediator.base import BaseCommands
from core.infrastructure.mediator.handlers.commands import CommandHandler


@dataclass(frozen=True)
class MainPageCommand(BaseCommands):
    flower: str | None = field(default=None)


@dataclass(frozen=True)
class MainPageCommandHandler(CommandHandler[MainPageCommand, Flower]):
    categories_service: BaseCategoriesService
    favorite_products_service_ids: BaseFavoriteProductsIdsService
    products_service: BaseProductsService

    def handle(
        self,
        command: MainPageCommand,
    ) -> Flower:
        favorite_products_ids = None
        if command.is_authenticated:
            favorite_products_ids = (
                self.favorite_products_service_ids.get_favorite_products_ids(
                    command.username,
                )
            )  # INFO: only ids of all products which mark as favorite

        categories = (
            self.categories_service.get_all_products_categories()
        )  # INFO: just all categories of products
        products = self.products_service.get_filtered_products(
            command.filters,
        )  # INFO: should work even without filters

        return favorite_products_ids, categories, products