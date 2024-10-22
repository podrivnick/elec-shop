from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import List

from django.db.models import QuerySet

from core.apps.carts_products.entities.review import ReviewEntity
from core.apps.carts_products.models.review import Reviews


@dataclass
class BaseQueryGetReviewsService(ABC):
    @abstractmethod
    def get_reviews_product(self) -> List[ReviewEntity]:
        raise NotImplementedError()

    @abstractmethod
    def get_review_product_by_user(self) -> List[ReviewEntity]:
        raise NotImplementedError()

    @abstractmethod
    def get_review_by_product_model(self) -> QuerySet[Reviews]:
        raise NotImplementedError()


@dataclass
class BaseCommandReviewsService(ABC):
    @abstractmethod
    def create_review_product(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete_review_product(self) -> None:
        raise NotImplementedError()


@dataclass
class BaseQueryLikesReviewService(ABC):
    @abstractmethod
    def get_liked_review(self):
        raise NotImplementedError()

    @abstractmethod
    def filter_reviews_by_user(self):
        raise NotImplementedError()

    @abstractmethod
    def filter_likes_by_review_product(self):
        raise NotImplementedError()


@dataclass
class BaseCommandLikesReviewService(ABC):
    @abstractmethod
    def update_likes_review(self) -> int:
        raise NotImplementedError()
