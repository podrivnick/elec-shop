from typing import Optional

from django.http import (
    HttpRequest,
    HttpResponse,
)
from ninja import Router

from core.api.schemas import SuccessResponse
from core.api.v1.carts_products.dto.base import DTOCartPageAPI
from core.api.v1.carts_products.dto.extractors import extract_cart_page_dto
from core.api.v1.carts_products.renders import render_cart
from core.api.v1.main.dto.responses import DTOResponseCartAPI
from core.infrastructure.di.main import init_container
from core.infrastructure.exceptions.base import BaseAppException
from core.infrastructure.mediator.mediator import Mediator


router = Router(tags=["cart"])


@router.get(
    "/cart/{product}",
    url_name="cart",
)
def cart(
    request: HttpRequest,
    product: Optional[str],
) -> HttpResponse:
    """API: Загрузка страницы товара."""
    container = init_container()
    mediator: Mediator = container.resolve(Mediator)

    cart_page_dto: DTOCartPageAPI = extract_cart_page_dto(
        request=request,
        product=product,
    )

    try:
        dto_response_cart_api: DTOResponseCartAPI = mediator.handle_command(
            CartPageCommand(  # noqa
                is_authenticated=cart_page_dto.is_authenticated,
                username=cart_page_dto.username,
                product_slug=cart_page_dto.product_slug,
            ),
        )[0]
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.message},
        )

    return render_cart(
        request=request,
        response=SuccessResponse(result=dto_response_cart_api),
        template="carts_products/cart_product.html",
    )
