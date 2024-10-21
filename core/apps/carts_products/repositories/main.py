from dataclasses import dataclass
from typing import (
    List,
    Optional,
)

from django.db.models import QuerySet

from core.apps.carts_products.models.review import (
    LikesReviews,
    Reviews,
)
from core.apps.carts_products.repositories.base import (
    BaseCommandLikeReviewsRepository,
    BaseQueryLikeReviewsRepository,
)
from core.apps.main.models.products import Products
from core.apps.users.models import User


@dataclass(frozen=True, eq=False)
class ORMQueryLikeReviewsRepository(BaseQueryLikeReviewsRepository):
    def filter_liked_review(
        self,
        user: User,
        id_product: Optional[int],
        reviews_ids: List[int],
    ) -> QuerySet[LikesReviews]:
        return LikesReviews.objects.filter(
            user=user,
            id_product=id_product,
            review_id__in=reviews_ids,
        ).select_related("id_product", "user")

    def get_review_by_product(
        self,
        product: QuerySet[Products],
        review_id: Optional[str],
    ) -> QuerySet[Reviews]:
        return Reviews.objects.get(id_product=product, pk=review_id)

    def filter_likes_by_review_product(
        self,
        user: QuerySet[User],
        product: QuerySet[Products],
        review: QuerySet[Reviews],
    ) -> QuerySet[Reviews]:
        return LikesReviews.objects.filter(
            user=user,
            id_product=product,
            review_id=review,
        ).first()


@dataclass(frozen=True, eq=False)
class ORMCommandLikeReviewsRepository(BaseCommandLikeReviewsRepository):
    def delete_likes(
        self,
        like_model: LikesReviews,
    ) -> None:
        like_model.delete()

    def create_likes(
        self,
        user: QuerySet[User],
        product: QuerySet[Products],
        review: QuerySet[Reviews],
    ) -> None:
        LikesReviews.objects.create(
            user=user,
            id_product=product,
            review_id=review,
        )
