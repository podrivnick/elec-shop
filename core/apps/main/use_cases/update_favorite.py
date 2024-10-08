from dataclasses import (
    dataclass,
    field,
)

from core.apps.common.exceptions.main import (
    AuthenticationError,
    UserNotFoundError,
)
from core.apps.common.services.base import BaseQueryGetUserModelService
from core.apps.main.exceptions.main import (
    DatabaseFavoriteError,
    FavoriteProductError,
)
from core.apps.main.services.update_favorite.base import (
    BaseCommandUpdateFavoriteProductsService,
    BaseQueryUpdateFavoriteProductsService,
)
from core.infrastructure.mediator.base import BaseCommands
from core.infrastructure.mediator.handlers.commands import CommandHandler


@dataclass(frozen=True)
class UpdateFavoritePageCommand(BaseCommands):
    product_id: int
    is_authenticated: str | None = field(default=None)
    username: str | None = field(default=None)


@dataclass(frozen=True)
class UpdateFavoritePageCommandHandler(
    CommandHandler[UpdateFavoritePageCommand, str],
):
    query_get_user_model_by_username: BaseQueryGetUserModelService
    query_update_favorite_product_service: BaseQueryUpdateFavoriteProductsService
    command_update_favorite_product_service: BaseCommandUpdateFavoriteProductsService

    def handle(
        self,
        command: UpdateFavoritePageCommand,
    ) -> None:
        if not command.is_authenticated:
            raise AuthenticationError("User is not authenticated.")

        try:
            is_product_in_favorite = self.query_update_favorite_product_service.check_product_in_favorite_is_exist(
                username=command.username,
                product_id=command.product_id,
            )
        except Exception as e:
            raise DatabaseFavoriteError("Error checking product in favorites.") from e

        if is_product_in_favorite:
            try:
                self.command_update_favorite_product_service.delete_product_from_favorite(
                    username=command.username,
                    product_id=command.product_id,
                )
            except Exception as e:
                raise FavoriteProductError(
                    "Error deleting product from favorites.",
                ) from e
        else:
            try:
                user = self.query_get_user_model_by_username.get_usermodel_by_username(
                    username=command.username,
                )
                if user is None:
                    raise UserNotFoundError(f"User '{command.username}' not found.")

                self.command_update_favorite_product_service.add_product_to_favorite(
                    user=user,
                    product_id=command.product_id,
                )
            except Exception as e:
                raise FavoriteProductError("Error adding product to favorites.") from e
