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
from core.api.v1.main.dto.responses import (
    DTOResponseFavoriteAPI,
    DTOResponseIndexAPI,
    DTOResponseInformationAPI,
)


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


def render_favorites(
    request: HttpRequest,
    response: SuccessResponse[DTOResponseFavoriteAPI],
    template: Template,
) -> HttpResponse:
    """Возвращает либо JSON-ответ, либо HTML в зависимости от типа запроса."""
    if request.headers.get("Content-Type") == "application/json":
        return JsonResponse(
            {
                "status": response.status,
                "result": {
                    "products": response.result.products,
                },
            },
        )
    else:
        return render(
            request,
            template,
            {
                "products": response.result.products,
            },
        )


def render_update_favorite(
    request: HttpRequest,
    response: SuccessResponse,
    template: Template,
) -> HttpResponse:
    """Возвращает либо JSON-ответ, либо HTML в зависимости от типа запроса."""
    if request.headers.get("Content-Type") == "application/json":
        return JsonResponse(
            {
                "status": response.status,
                "result": {
                    "message": response.result,
                },
            },
        )
    else:
        return render(
            request,
            template,
            {
                "message": response.result,
            },
        )


def render_information(
    request: HttpRequest,
    response: SuccessResponse[DTOResponseInformationAPI],
    template: Template,
) -> HttpResponse:
    """Возвращает либо JSON-ответ, либо HTML в зависимости от типа запроса."""
    if request.headers.get("Content-Type") == "application/json":
        return JsonResponse(
            {
                "status": response.status,
                "result": {
                    "info": response.result.info,
                },
            },
        )
    else:
        return render(
            request,
            template,
            {
                "info": response.result.info,
            },
        )
