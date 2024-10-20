from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import List

from core.apps.carts_products.entities.review import ReviewEntity


@dataclass
class BaseQueryGetReviewsService(ABC):
    @abstractmethod
    def get_reviews_product(self) -> List[ReviewEntity]:
        raise NotImplementedError()

    @abstractmethod
    def get_review_product_by_user(self) -> List[ReviewEntity]:
        raise NotImplementedError()


@dataclass
class BaseCommandReviewsService(ABC):
    @abstractmethod
    def create_review_product(self) -> List[ReviewEntity]:
        raise NotImplementedError()


@dataclass
class BaseQueryLikesReviewService(ABC):
    @abstractmethod
    def get_liked_review(self):
        raise NotImplementedError()

    @abstractmethod
    def filter_reviews_by_user(self):
        raise NotImplementedError()
