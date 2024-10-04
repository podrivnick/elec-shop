from dataclasses import (
    dataclass,
    field,
)

from core.infrastructure.mediator.base import BaseCommands
from core.infrastructure.mediator.handlers.commands import CommandHandler


class BaseChangerFavoriteService:
    pass


class BaseFavoriteProductsExistService:
    pass


@dataclass(frozen=True)
class UpdateFavoritePageCommand(BaseCommands):
    flower: str | None = field(default=None)


@dataclass(frozen=True)
class UpdateFavoritePageCommandHandler(
    CommandHandler[UpdateFavoritePageCommand, str],
):
    product_in_favorite: BaseFavoriteProductsExistService
    add_or_delete_favorite: BaseChangerFavoriteService

    def handle(
        self,
        command: UpdateFavoritePageCommand,
    ) -> None:
        if command.is_authenticated:
            is_product_in_favorite: bool = (
                self.product_in_favorite.check_product_in_favorite(
                    command.username,
                    command.product_id,
                )
            )  # INFO: varafication product in favorite by usernane and product id

            add_product_to_favorite_or_delete_from_favorite = (
                self.add_or_delete_favorite.add_product_to_favorite_or_delete(
                    is_product_in_favorite,
                    command.username,
                    command.product_id,
                )
            )  # INFO: depends of is_product_in_favorite delete or create favorite

            return add_product_to_favorite_or_delete_from_favorite
