from django.http import (
    HttpRequest,
    HttpResponse,
    JsonResponse,
)
from django.shortcuts import render

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
    if request.headers.get("Content-Type") == "application/json":
        return JsonResponse(
            {
                "status": response.status,
                "result": {
                    "message": "packet has updated",
                    "carts_items_user": response.result.carts_items_user,
                },
            },
        )
    else:
        return render(
            request,
            template,
            {
                "message": "packet has updated",
                "carts_items_user": response.result.carts_items_user,
            },
        )
