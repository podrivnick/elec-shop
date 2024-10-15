from django.http import (
    HttpRequest,
    HttpResponse,
    JsonResponse,
)

from core.api.schemas import (
    SuccessResponse,
    Template,
)
from core.api.v1.packet.dto.responses import (
    DTOResponseAddPacketAPI,
    DTOResponseUpdatePacketAPI,
)


def render_add_packet(
    request: HttpRequest,
    response: SuccessResponse[DTOResponseAddPacketAPI],
    template: Template = None,
) -> HttpResponse:
    """Возвращает либо JSON-ответ, либо HTML в зависимости от типа запроса."""
    return JsonResponse(
        {
            "message": "packet has updated",
            "carts_items_user": response.result.carts_items_user,
        },
    )


def render_delete_packet(
    request: HttpRequest,
    response: SuccessResponse[DTOResponseUpdatePacketAPI],
    template: Template = None,
) -> HttpResponse:
    """Возвращает либо JSON-ответ, либо HTML в зависимости от типа запроса."""
    return JsonResponse(
        {
            "message": "packet has updated",
            "new_quantity": response.result.new_quantity,
            "carts_items_user": response.result.carts_items_user,
        },
    )


def render_change_packet(
    request: HttpRequest,
    response: SuccessResponse[DTOResponseUpdatePacketAPI],
    template: Template = None,
) -> HttpResponse:
    """Возвращает либо JSON-ответ, либо HTML в зависимости от типа запроса."""
    return JsonResponse(
        {
            "message": "packet has updated",
            "new_quantity": response.result.new_quantity,
            "carts_items_user": response.result.carts_items_user,
        },
    )
