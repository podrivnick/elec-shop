from dataclasses import dataclass
from typing import (
    List,
    Optional,
)

from core.apps.carts_products.entities.review import ReviewEntity
from core.apps.carts_products.models.review import (
    LikesReviews,
    Reviews,
)
from core.apps.carts_products.services.base import (
    BaseQueryGetReviewsService,
    BaseQueryLikesReviewService,
)
from core.apps.users.models import User


@dataclass
class ORMQueryGetReviewsService(BaseQueryGetReviewsService):
    def get_reviews_product(
        self,
        id_product: Optional[int],
    ) -> List[ReviewEntity]:
        reviews = Reviews.objects.filter(id_product=id_product).select_related(
            "id_product",
            "user",
        )

        return [review.to_entity() for review in reviews]


@dataclass
class ORMQueryLikesReviewService(BaseQueryLikesReviewService):
    def get_liked_review(
        self,
        user: User,
        id_product: Optional[int],
        reviews: List[ReviewEntity],
    ) -> List[int]:
        review_ids = [review.pk for review in reviews]

        liked_reviews = LikesReviews.objects.filter(
            user=user,
            id_product=id_product,
            opinion_id__in=review_ids,
        ).select_related("id_product", "user")

        liked_reviews_dict = {like.opinion_id: like for like in liked_reviews}

        list_liked_opinion = [liked_reviews_dict.get(review.pk) for review in reviews]

        return list_liked_opinion

    def filter_reviews_by_user(
        self,
        user: User,
        reviews: List[ReviewEntity],
    ) -> None:
        index_to_move = next(
            (i for i, item in enumerate(reviews) if item.user == user),
            None,
        )

        # Если мнение пользователя найдено (индекс не равен None)
        if index_to_move is not None:
            # Удалить элемент из текущей позиции и вставить его в начало списка
            reviews.insert(0, reviews.pop(index_to_move))

        return reviews
