from django.contrib import messages
from django.http import (
    HttpRequest,
    HttpResponse,
)
from ninja import Router

from core.api.schemas import SuccessResponse
from core.api.v1.orders.dto.base import DTOCreateOrderAPI
from core.api.v1.orders.dto.extractors import extract_create_order_dto
from core.api.v1.orders.dto.responses import DTOResponseOrderAPI
from core.api.v1.orders.renders import render_order
from core.apps.orders.config import SUCCESSFUL_ORDER
from core.apps.orders.use_cases.order import OrderCommand
from core.infrastructure.di.main import init_container
from core.infrastructure.exceptions.base import BaseAppException
from core.infrastructure.mediator.mediator import Mediator


router = Router(tags=["order"])


@router.post(
    "/order",
    url_name="order",
)
def order(
    request: HttpRequest,
) -> HttpResponse:
    """API: Сoздание заказа."""
    container = init_container()
    mediator: Mediator = container.resolve(Mediator)

    order_dto: DTOCreateOrderAPI = extract_create_order_dto(
        request=request,
    )

    try:
        dto_response_order_api: DTOResponseOrderAPI = mediator.handle_command(
            OrderCommand(
                is_authenticated=order_dto.is_authenticated,
                username=order_dto.username,
                first_name=order_dto.first_name,
                last_name=order_dto.last_name,
                email=order_dto.email,
                phone=order_dto.phone,
                delivery_address=order_dto.delivery_address,
                required_delivery=order_dto.required_delivery,
                payment_on_get=order_dto.payment_on_get,
                total_price=order_dto.total_price,
            ),
        )[0]
    except BaseAppException as exception:
        messages.success(request, f"{exception}")

        return render_order(
            request=request,
            response=SuccessResponse(result=dto_response_order_api),
            template="carts_products:finalize_product",
        )

    messages.success(request, SUCCESSFUL_ORDER)

    return render_order(
        request=request,
        response=SuccessResponse(result=dto_response_order_api),
        template="main_favorite:index",
    )
