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
from core.api.v1.main.dto.responses import DTOResponseIndexAPI


def render_index(
    request: HttpRequest,
    response: SuccessResponse[DTOResponseIndexAPI],
    template: Template,
) -> HttpResponse:
    """Возвращает либо JSON-ответ, либо HTML в зависимости от типа запроса."""
    if request.headers.get("Content-Type") == "application/json":
        return JsonResponse(
            {
                "status": response.status,
                "result": {
                    "favorites": response.result.favorites,
                    "categories": response.result.categories,
                    "is_search_failed": response.result.is_search_failed,
                    "products": response.result.products,
                },
            },
        )
    else:
        return render(
            request,
            template,
            {
                "favorites": response.result.favorites,
                "categories": response.result.categories,
                "is_search_failed": response.result.is_search_failed,
                "products": response.result.products,
            },
        )
