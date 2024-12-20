from dataclasses import (
    dataclass,
    field,
)
from typing import (
    List,
    Optional,
)

from core.api.v1.main.dto.base import BaseDTOAPI
from core.apps.carts_products.entities.review import ReviewEntity
from core.apps.carts_products.schemas.main import ReviewDataSchema
from core.apps.main.entities.product import ProductEntity
from core.apps.orders.schemas.main import OrderSchema
from core.apps.packet.entities.cart import CartEntity


@dataclass(frozen=True, eq=False)
class DTOResponseCartAPI(BaseDTOAPI):
    products: ProductEntity | None = field(default=None)
    favorites: List[int] | None = field(default_factory=list, kw_only=True)
    count_all_reviews: Optional[int] | None = field(default=None)
    liked_objects: List[int] | None = field(default=list)
    reviews: List[ReviewEntity] | None = field(default=None)
    form: ReviewDataSchema | None = field(default=None)


@dataclass(frozen=True, eq=False)
class DTOResponseReviewsAPI(BaseDTOAPI):
    product: ProductEntity | None = field(default=None)
    liked_objects: List[int] | None = field(default=list)
    reviews: List[ReviewEntity] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class DTOResponseCreateReviewAPI(BaseDTOAPI):
    product_slug: Optional[str] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class DTOResponseChangeReviewAPI(BaseDTOAPI):
    updated_likes: Optional[int] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class DTOResponseDeleteReviewAPI(BaseDTOAPI):
    slug_product: Optional[str] | None = field(default=None)


@dataclass(frozen=True, eq=False)
class DTOResponseFinalizeAPI(BaseDTOAPI):
    carts: List[CartEntity] | None = field(default=None)
    total_price: Optional[int] | None = field(default=None)
    form: OrderSchema | None = field(default=None)
