from dataclasses import (
    dataclass,
    field,
)

from src.domain.flowers.entities.flower import (
    BaseFavoriteProductsIdsService,
    BaseFavoriteProductsService,
    BaseProductsService,
    Flower,
)

from core.infrastructure.mediator.base import BaseCommands
from core.infrastructure.mediator.handlers.commands import CommandHandler


@dataclass(frozen=True)
class FavoritePageCommand(BaseCommands):
    flower: str | None = field(default=None)


@dataclass(frozen=True)
class FavoritePageCommandHandler(CommandHandler[FavoritePageCommand, Flower]):
    favorite_products_service: BaseFavoriteProductsService
    favorite_products_service_ids: BaseFavoriteProductsIdsService
    products_service: BaseProductsService

    def handle(
        self,
        command: FavoritePageCommand,
    ) -> Flower:
        if command.is_authenticated:
            favorite_products = (
                self.favorite_products_service_ids.get_favorite_products_ids(
                    command.username,
                )
            )  # INFO: only ids of all products which mark as favorite

        products = self.products_service.get_filtered_products(
            command.filters,
        )  # INFO: should work even without filters
        favorite_products = self.favorite_products_service.get_favorite_products(
            command.products,
        )  # INFO: products which in favorite of user

        return favorite_products, favorite_products, products
