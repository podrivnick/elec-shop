from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from django.db.models import QuerySet

from core.apps.carts_products.models.review import (
    LikesReviews,
    Reviews,
)


@dataclass(frozen=True, eq=False)
class BaseQueryLikeReviewsRepository(ABC):
    @abstractmethod
    def filter_liked_review(self) -> QuerySet[LikesReviews]:
        raise NotImplementedError()

    @abstractmethod
    def get_review_by_product(self) -> QuerySet[Reviews]:
        raise NotImplementedError()

    @abstractmethod
    def filter_likes_by_review_product(self) -> QuerySet[Reviews]:
        raise NotImplementedError()


@dataclass(frozen=True, eq=False)
class BaseCommandLikeReviewsRepository(ABC):
    @abstractmethod
    def delete_likes(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def create_likes(self) -> None:
        raise NotImplementedError()
