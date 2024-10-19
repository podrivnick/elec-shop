from dataclasses import dataclass
from typing import (
    List,
    Optional,
)

from django.db.models import QuerySet

from core.apps.carts_products.models.review import LikesReviews
from core.apps.carts_products.repositories.base import BaseQueryLikeReviewsRepository
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
