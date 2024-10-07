from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Dict,
    List,
)

from core.apps.common.utils.context import convert_to_context_dict
from core.apps.main.entities.product import ProductEntity
from core.apps.main.services.base import (
    BaseAllProductsService,
    BaseFavoriteProductsIdsService,
)
from core.apps.main.services.favorites.base import BaseFavoriteProductsIdsFilterService
from core.infrastructure.mediator.base import BaseCommands
from core.infrastructure.mediator.handlers.commands import CommandHandler


@dataclass(frozen=True)
class FavoritePageCommand(BaseCommands):
    is_authenticated: bool = field(default=False)
    username: str | None = field(default=None)


@dataclass(frozen=True)
class FavoritePageCommandHandler(CommandHandler[FavoritePageCommand, str]):
    favorite_products_service_ids: BaseFavoriteProductsIdsService
    get_all_products_service: BaseAllProductsService
    products_service: BaseFavoriteProductsIdsFilterService

    def handle(
        self,
        command: FavoritePageCommand,
    ) -> Dict[str, List[ProductEntity]]:
        if not command.is_authenticated:
            return []

        favorite_products_ids = (
            self.favorite_products_service_ids.get_ids_products_in_favorite(
                command.username,
            )
        )

        if not favorite_products_ids:
            return []

        products = self.get_all_products_service.get_all_products()
        filtered_products = self.products_service.get_filtered_products_by_favorite_ids(
            products=products,
            ids_products_in_favorite=favorite_products_ids,
        )

        return convert_to_context_dict(products=filtered_products)
