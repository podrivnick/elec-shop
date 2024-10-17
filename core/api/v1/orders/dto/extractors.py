from typing import Optional

from django.http import HttpRequest
from ninja import Query

from core.api.v1.main.dto.base import DTOMainPageAPI
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
