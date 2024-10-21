from typing import Optional

from django.http import HttpRequest

import orjson

from core.api.v1.carts_products.dto.base import (
    DTOCartPageAPI,
    DTOReviewChangeAPI,
    DTOReviewCreateAPI,
    DTOReviewPageAPI,
)


def extract_cart_page_dto(
    request: HttpRequest,
    product: Optional[str],
) -> DTOCartPageAPI:
    is_authenticated = request.user.is_authenticated
    username = request.user.username if is_authenticated else None

    return DTOCartPageAPI(
        is_authenticated=is_authenticated,
        username=username,
        product_slug=product,
    )


def extract_reviews_page_dto(
    request: HttpRequest,
    product: Optional[str],
) -> DTOReviewPageAPI:
    is_authenticated = request.user.is_authenticated
    username = request.user.username if is_authenticated else None

    return DTOReviewPageAPI(
        is_authenticated=is_authenticated,
        username=username,
        product_slug=product,
    )


def extract_create_review_dto(
    request: HttpRequest,
) -> DTOReviewCreateAPI:
    review = request.POST.get("message")
    id_product = request.POST.get("id_product")
    product_slug = request.POST.get("slug_product")

    is_authenticated = request.user.is_authenticated
    username = request.user.username if is_authenticated else None

    return DTOReviewCreateAPI(
        is_authenticated=is_authenticated,
        username=username,
        review=review,
        product_slug=product_slug,
        id_product=id_product,
    )


def extract_change_review_dto(
    request: HttpRequest,
) -> DTOReviewChangeAPI:
    data = orjson.loads(request.body)

    product_id = data["data"][1]
    review_id = data["data"][2]

    is_authenticated = request.user.is_authenticated
    username = request.user.username if is_authenticated else None

    return DTOReviewChangeAPI(
        is_authenticated=is_authenticated,
        username=username,
        product_id=product_id,
        review_id=review_id,
    )
