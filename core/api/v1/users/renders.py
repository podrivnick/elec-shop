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
from core.api.v1.users.dto.responses import DTOResponseLoginAPI


def render_login(
    request: HttpRequest,
    response: SuccessResponse[DTOResponseLoginAPI],
    template: Template,
) -> HttpResponse:
    """Возвращает либо JSON-ответ, либо HTML в зависимости от типа запроса."""
    if request.headers.get("Content-Type") == "application/json":
        return JsonResponse(
            {
                "status": response.status,
                "result": {
                    "form": response.result,
                },
            },
        )
    else:
        return render(
            request,
            template,
            {
                "form": response.result,
            },
        )
