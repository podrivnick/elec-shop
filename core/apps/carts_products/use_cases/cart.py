from dataclasses import (
    dataclass,
    field,
)
from typing import (
    List,
    Optional,
)

from core.api.v1.carts_products.dto.responses import DTOResponseCartAPI
from core.apps.carts_products.entities.review import ReviewEntity
from core.apps.carts_products.schemas.main import ReviewDataSchema
from core.apps.carts_products.services.base import (
    BaseQueryGetReviewsService,
    BaseQueryLikesReviewService,
)
from core.apps.common.services.base import BaseQueryGetUserModelService
from core.apps.main.entities.product import ProductEntity
from core.apps.main.services.base import (
    BaseAllProductsService,
    BaseFavoriteProductsIdsService,
)
from core.apps.main.services.main.base import BaseProductsService
from core.infrastructure.mediator.base import BaseCommands
from core.infrastructure.mediator.handlers.commands import CommandHandler


@dataclass(frozen=True)
class CartPageCommand(BaseCommands):
    is_authenticated: bool = field(default=False)
    username: Optional[str] | None = field(default=None)
    product_slug: Optional[str] | None = field(default=None)


@dataclass(frozen=True)
class CartPageCommandHandler(CommandHandler[CartPageCommand, str]):
    query_get_all_products_service: BaseAllProductsService
    query_products_service: BaseProductsService
    query_reviews_filtered_service: BaseQueryGetReviewsService
    query_favorite_products_service_ids: BaseFavoriteProductsIdsService
    query_likes_filter_service: BaseQueryLikesReviewService
    query_get_user_model_by_username: BaseQueryGetUserModelService

    def handle(
        self,
        command: CartPageCommand,
    ) -> DTOResponseCartAPI:
        products = self.query_get_all_products_service.get_all_products()
        product_entity: ProductEntity = (
            self.query_products_service.get_filtered_product_by_slug(
                products=products,
                slug=command.product_slug,
            )
        )

        reviews: List[ReviewEntity] = (
            self.query_reviews_filtered_service.get_reviews_product(
                id_product=product_entity.id_product,
            )
        )
        count_all_reviews = self.count_reviews(reviews=reviews)

        favorites_ids = (
            self.query_favorite_products_service_ids.get_ids_products_in_favorite(
                username=command.username,
            )
        )
        list_liked_review = []
        if reviews and command.is_authenticated:
            user = self.query_get_user_model_by_username.get_usermodel_by_username(
                username=command.username,
            )

            list_liked_review = self.query_likes_filter_service.get_liked_review(
                user=user,
                id_product=product_entity.id_product,
                reviews=reviews,
            )
            reviews = self.query_likes_filter_service.filter_reviews_by_user(
                user=user,
                reviews=reviews,
            )

        return DTOResponseCartAPI(
            products=product_entity,
            favorites=favorites_ids,
            count_all_reviews=count_all_reviews,
            liked_objects=list_liked_review,
            reviews=reviews,
            form=ReviewDataSchema(),
        )

    @staticmethod
    def count_reviews(reviews: List[ReviewEntity]) -> int:
        return len(reviews)
