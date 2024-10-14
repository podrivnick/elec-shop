from django.http import (
    HttpRequest,
    HttpResponse,
    JsonResponse,
)

from core.api.schemas import (
    SuccessResponse,
    Template,
)
from core.api.v1.packet.dto.responses import DTOResponseAddPacketAPI


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
