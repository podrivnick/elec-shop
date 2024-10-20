from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.api.v1.carts_products.dto.responses import DTOResponseCreateReviewAPI
from core.apps.carts_products.exceptions.main import UserAlreadyWriteReviewError
from core.apps.carts_products.services.base import (
    BaseCommandReviewsService,
    BaseQueryGetReviewsService,
)
from core.apps.common.exceptions.main import AuthenticationError
from core.apps.common.services.base import BaseQueryGetUserModelService
from core.apps.main.repositories.base import BaseQueryProductRepository
from core.apps.packet.exceptions.main import DatabaseCartError
from core.infrastructure.mediator.base import BaseCommands
from core.infrastructure.mediator.handlers.commands import CommandHandler


@dataclass(frozen=True)
class CreateReviewCommand(BaseCommands):
    is_authenticated: bool = field(default=False)
    username: Optional[str] | None = field(default=None)
    product_slug: Optional[str] | None = field(default=None)
    id_product: Optional[int] | None = field(default=None)
    review: Optional[str] | None = field(default=None)


@dataclass(frozen=True)
class CreateReviewCommandHandler(CommandHandler[CreateReviewCommand, str]):
    query_get_user_model_by_username: BaseQueryGetUserModelService
    query_get_review_service: BaseQueryGetReviewsService
    query_product_repository: BaseQueryProductRepository
    command_update_review_service: BaseCommandReviewsService

    def handle(
        self,
        command: CreateReviewCommand,
    ) -> DTOResponseCreateReviewAPI:
        if not command.is_authenticated:
            raise AuthenticationError("User is not authenticated.")
        user_model = self.query_get_user_model_by_username.get_usermodel_by_username(
            username=command.username,
        )

        reviews_entity = self.query_get_review_service.get_review_product_by_user(
            id_product=command.id_product,
            user=user_model,
        )
        if reviews_entity:
            raise UserAlreadyWriteReviewError(
                f"{command.username} Already Write Review.",
            )

        product_model = self.query_product_repository.filter_product_by_slug(
            slug=command.product_slug,
        )

        try:
            self.command_update_review_service.create_review_product(
                product_object=product_model[0],
                user=user_model,
                review=command.review,
            )
        except Exception:
            raise DatabaseCartError("Error While Updating Datebase.")

        return DTOResponseCreateReviewAPI(
            product_slug=command.product_slug,
        )
