from dataclasses import (
    dataclass,
    field,
)

from src.domain.flowers.entities.flower import (
    BaseCategoriesService,
    BaseFavoriteProductsService,
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
    favorite_products_service: BaseFavoriteProductsService
    products_service: BaseProductsService

    def handle(
        self,
        command: MainPageCommand,
    ) -> Flower:
        if command.is_authenticated:
            favorite_products = (
                self.favorite_products_service.get_favorite_products_ids(
                    command.username,
                )
            )

        categories = self.categories_service.get_all_products_categories()
        products = self.products_service.get_filtered_products(command.filters)

        return favorite_products, categories, products
