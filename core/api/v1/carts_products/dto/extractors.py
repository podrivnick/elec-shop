from typing import Optional

from django.http import HttpRequest

from core.api.v1.carts_products.dto.base import DTOCartPageAPI


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
