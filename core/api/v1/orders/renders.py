from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.shortcuts import redirect
from django.urls import reverse

from core.api.schemas import (
    SuccessResponse,
    Template,
)
from core.api.v1.orders.dto.responses import DTOResponseOrderAPI


def render_order(
    request: HttpRequest,
    response: SuccessResponse[DTOResponseOrderAPI],
    template: Template,
) -> HttpResponse:
    """Возвращает либо JSON-ответ, либо HTML в зависимости от типа запроса."""

    if template == "index":
        return redirect(reverse(f"v1:{template}", kwargs={"category_slug": "all"}))

    return redirect(reverse(f"v1:{template}"))
