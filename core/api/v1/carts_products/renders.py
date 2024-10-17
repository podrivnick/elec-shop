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
from core.api.v1.main.dto.responses import DTOResponseCartAPI


def render_cart(
    request: HttpRequest,
    response: SuccessResponse[DTOResponseCartAPI],
    template: Template,
) -> HttpResponse:
    """Возвращает либо JSON-ответ, либо HTML в зависимости от типа запроса."""
    if request.headers.get("Content-Type") == "application/json":
        return JsonResponse(
            {
                "status": response.status,
                "result": {
                    "products": response.result.products,
                    "count_all_opinions": response.result.count_all_opinions,
                    "favorites": response.result.favorites,
                    "liked_objects": response.result.liked_objects,
                    "opinions": response.result.opinions,
                    "form": response.result.form,
                },
            },
        )
    else:
        return render(
            request,
            template,
            {
                "products": response.result.products,
                "count_all_opinions": response.result.count_all_opinions,
                "favorites": response.result.favorites,
                "liked_objects": response.result.liked_objects,
                "opinions": response.result.opinions,
                "form": response.result.form,
            },
        )
