from typing import Optional

from django.http import HttpRequest
from ninja import Query

import orjson

from core.api.v1.main.dto.base import (
    DTOFavoritePageAPI,
    DTOMainPageAPI,
    DTOUpdateFavoriteProduct,
)
from core.api.v1.main.schemas import FiltersProductsSchema


def extract_main_page_dto(
    request: HttpRequest,
    filters: Query[FiltersProductsSchema],
    category_slug: Optional[str],
) -> DTOMainPageAPI:
    page_number = request.GET.get("page")
    is_authenticated = request.user.is_authenticated
    username = request.user.username if is_authenticated else None

    return DTOMainPageAPI(
        is_authenticated=is_authenticated,
        username=username,
        filters=filters,
        page_number=page_number,
        category_slug=category_slug,
    )


def extract_favorite_page_dto(
    request: HttpRequest,
) -> DTOFavoritePageAPI:
    is_authenticated = request.user.is_authenticated
    username = request.user.username if is_authenticated else None

    return DTOFavoritePageAPI(
        is_authenticated=is_authenticated,
        username=username,
    )


def extract_save_favorite_dto(
    request: HttpRequest,
) -> DTOUpdateFavoriteProduct:
    is_authenticated = request.user.is_authenticated
    username = request.user.username if is_authenticated else None

    json_request_data = orjson.loads(request.body)
    product_id = json_request_data["data"][1]

    return DTOUpdateFavoriteProduct(
        product_id=product_id,
        is_authenticated=is_authenticated,
        username=username,
    )
