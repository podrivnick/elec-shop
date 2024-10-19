from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from django.db.models import QuerySet

from core.apps.carts_products.models.review import LikesReviews


@dataclass(frozen=True, eq=False)
class BaseQueryLikeReviewsRepository(ABC):
    @abstractmethod
    def filter_liked_review(self) -> QuerySet[LikesReviews]:
        raise NotImplementedError()
