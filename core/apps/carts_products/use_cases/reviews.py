from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.api.v1.carts_products.dto.responses import (
    DTOResponseChangeReviewAPI,
    DTOResponseCreateReviewAPI,
    DTOResponseDeleteReviewAPI,
)
from core.apps.carts_products.exceptions.main import (
    ProductNotFoundError,
    ReviewNotFoundError,
    UserAlreadyWriteReviewError,
)
from core.apps.carts_products.services.base import (
    BaseCommandLikesReviewService,
    BaseCommandReviewsService,
    BaseQueryGetReviewsService,
    BaseQueryLikesReviewService,
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


@dataclass(frozen=True)
class ChangeLikesReviewCommand(BaseCommands):
    is_authenticated: bool = field(default=False)
    username: Optional[str] | None = field(default=None)
    product_id: Optional[str] | None = field(default=None)
    review_id: Optional[int] | None = field(default=None)


@dataclass(frozen=True)
class ChangeLikesReviewCommandHandler(CommandHandler[ChangeLikesReviewCommand, str]):
    query_get_user_model_by_username: BaseQueryGetUserModelService
    query_product_repository: BaseQueryProductRepository
    query_get_review_service: BaseQueryGetReviewsService
    query_like_review_service: BaseQueryLikesReviewService
    command_likes_review_service: BaseCommandLikesReviewService

    def handle(
        self,
        command: ChangeLikesReviewCommand,
    ) -> DTOResponseChangeReviewAPI:
        if not command.is_authenticated:
            raise AuthenticationError("User is not authenticated.")
        user_model = self.query_get_user_model_by_username.get_usermodel_by_username(
            username=command.username,
        )

        product_model = self.query_product_repository.get_product_by_id(
            id_product=command.product_id,
        )
        if not product_model:
            raise ProductNotFoundError("Some Error In Product")

        review = self.query_get_review_service.get_review_by_product_model(
            product=product_model,
            review_id=command.review_id,
        )
        if not review:
            raise ReviewNotFoundError("That Review Not Exist")

        liked_review = self.query_like_review_service.filter_likes_by_review_product(
            user=user_model,
            product=product_model,
            review=review,
        )

        updated_likes = self.command_likes_review_service.update_likes_review(
            likes_model=liked_review,
            product=product_model,
            user=user_model,
            review=review,
        )

        return DTOResponseChangeReviewAPI(
            updated_likes=updated_likes,
        )


@dataclass(frozen=True)
class DeleteReviewCommand(BaseCommands):
    is_authenticated: bool = field(default=False)
    username: Optional[str] | None = field(default=None)
    slug_product: Optional[str] | None = field(default=None)
    pk_product: Optional[int] | None = field(default=None)


@dataclass(frozen=True)
class DeleteReviewCommandHandler(CommandHandler[DeleteReviewCommand, str]):
    query_get_user_model_by_username: BaseQueryGetUserModelService
    command_review_service: BaseCommandReviewsService

    def handle(
        self,
        command: DeleteReviewCommand,
    ) -> DTOResponseDeleteReviewAPI:
        if not command.is_authenticated:
            raise AuthenticationError("User is not authenticated.")
        user_model = self.query_get_user_model_by_username.get_usermodel_by_username(
            username=command.username,
        )

        self.command_review_service.delete_review_product(
            user=user_model,
            pk_product=command.pk_product,
        )

        return DTOResponseDeleteReviewAPI(
            slug_product=command.slug_product,
        )
