from dataclasses import dataclass
from datetime import date
from typing import (
    List,
    Optional,
)

from django.db.models import QuerySet

from core.apps.carts_products.entities.review import ReviewEntity
from core.apps.carts_products.models.review import (
    LikesReviews,
    Reviews,
)
from core.apps.carts_products.repositories.base import (
    BaseCommandLikeReviewsRepository,
    BaseQueryLikeReviewsRepository,
)
from core.apps.carts_products.services.base import (
    BaseCommandLikesReviewService,
    BaseCommandReviewsService,
    BaseQueryGetReviewsService,
    BaseQueryLikesReviewService,
)
from core.apps.main.models.products import Products
from core.apps.users.models import User


@dataclass
class ORMQueryGetReviewsService(BaseQueryGetReviewsService):
    query_filter_likes_review_repository: BaseQueryLikeReviewsRepository

    def get_reviews_product(
        self,
        id_product: Optional[int],
    ) -> List[ReviewEntity]:
        reviews = Reviews.objects.filter(id_product=id_product).select_related(
            "id_product",
            "user",
        )

        return [review.to_entity() for review in reviews]

    def get_review_product_by_user(
        self,
        id_product: Optional[int],
        user: QuerySet[User],
    ) -> List[ReviewEntity]:
        reviews = Reviews.objects.filter(
            id_product=id_product,
            user=user,
        )

        return [review.to_entity() for review in reviews]

    def get_review_by_product_model(
        self,
        product: QuerySet[Products],
        review_id: Optional[str],
    ) -> QuerySet[Reviews]:
        review = self.query_filter_likes_review_repository.get_review_by_product(
            product=product,
            review_id=review_id,
        )

        return review


@dataclass
class ORMCommandReviewsService(BaseCommandReviewsService):
    def create_review_product(
        self,
        product_object: QuerySet[Products],
        user: QuerySet[User],
        review: Optional[str],
    ) -> None:
        review = Reviews.objects.create(
            id_product=product_object,
            review=review,
            user=user,
            data_added=date.today(),
        )
        review.save()


@dataclass
class ORMQueryLikesReviewService(BaseQueryLikesReviewService):
    query_filter_likes_review_repository: BaseQueryLikeReviewsRepository

    def get_liked_review(
        self,
        user: User,
        id_product: Optional[int],
        reviews: List[ReviewEntity],
    ) -> List[int]:
        review_ids = [review.pk for review in reviews]

        liked_reviews = self.query_filter_likes_review_repository.filter_liked_review(
            user=user,
            id_product=id_product,
            reviews_ids=review_ids,
        )

        liked_reviews_dict = {like.review_id.pk: like for like in liked_reviews}

        list_liked_review = [liked_reviews_dict.get(review.pk) for review in reviews]

        return list_liked_review

    def filter_reviews_by_user(
        self,
        user: User,
        reviews: List[ReviewEntity],
    ) -> None:
        index_to_move = next(
            (i for i, item in enumerate(reviews) if item.user == user),
            None,
        )

        if index_to_move is not None:
            reviews.insert(0, reviews.pop(index_to_move))

        return reviews

    def filter_likes_by_review_product(
        self,
        user: QuerySet[User],
        product: QuerySet[Products],
        review: QuerySet[Reviews],
    ) -> QuerySet[LikesReviews]:
        is_review_liked = (
            self.query_filter_likes_review_repository.filter_likes_by_review_product(
                user=user,
                product=product,
                review=review,
            )
        )

        if is_review_liked:
            return is_review_liked


@dataclass
class ORMCommandLikesReviewService(BaseCommandLikesReviewService):
    command_likes_review_repository: BaseCommandLikeReviewsRepository

    def update_likes_review(
        self,
        likes_model: LikesReviews | None,
        product: QuerySet[Products],
        user: QuerySet[User],
        review: QuerySet[Reviews],
    ) -> int:
        if likes_model:
            self.command_likes_review_repository.delete_likes(like_model=likes_model)
            review.likes = review.likes - 1
            updated_likes = review.likes
        else:
            self.command_likes_review_repository.create_likes(
                user=user,
                product=product,
                review=review,
            )
            review.likes = review.likes + 1
            updated_likes = review.likes

        review.save()

        return updated_likes
