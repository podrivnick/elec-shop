from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import (
    redirect,
    render,
)
from django.urls import reverse

from core.api.schemas import (
    SuccessResponse,
    Template,
)
from core.api.v1.carts_products.dto.responses import (
    DTOResponseCartAPI,
    DTOResponseChangeReviewAPI,
    DTOResponseCreateReviewAPI,
    DTOResponseDeleteReviewAPI,
    DTOResponseFinalizeAPI,
    DTOResponseReviewsAPI,
)


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
                    "count_all_opinions": response.result.count_all_reviews,
                    "favorites": response.result.favorites,
                    "liked_objects": response.result.liked_objects,
                    "opinions": response.result.reviews,
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
                "count_all_opinions": response.result.count_all_reviews,
                "favorites": response.result.favorites,
                "liked_objects": response.result.liked_objects,
                "opinions": response.result.reviews,
                "form": response.result.form,
            },
        )


def render_reviews(
    request: HttpRequest,
    response: SuccessResponse[DTOResponseReviewsAPI],
    template: Template,
) -> HttpResponse:
    """Возвращает либо JSON-ответ, либо HTML в зависимости от типа запроса."""
    if request.headers.get("Content-Type") == "application/json":
        return JsonResponse(
            {
                "status": response.status,
                "result": {
                    "product": response.result.product,
                    "liked_objects": response.result.liked_objects,
                    "opinions": response.result.reviews,
                },
            },
        )
    else:
        return render(
            request,
            template,
            {
                "product": response.result.product,
                "liked_objects": response.result.liked_objects,
                "opinions": response.result.reviews,
            },
        )


def render_create_review(
    request: HttpRequest,
    response: SuccessResponse[DTOResponseCreateReviewAPI],
    template: Template = None,
) -> HttpResponse:
    """Перенаправление на html страницу."""

    return HttpResponseRedirect(
        reverse("v1:cart", args=[response.result.product_slug]),
    )


def render_change_review(
    request: HttpRequest,
    response: SuccessResponse[DTOResponseChangeReviewAPI],
    template: Template = None,
) -> HttpResponse:
    """Json Response."""

    return JsonResponse(
        {"likes_count": response.result.updated_likes},
    )


def render_delete_review(
    request: HttpRequest,
    response: SuccessResponse[DTOResponseDeleteReviewAPI],
    template: Template = None,
) -> HttpResponse:
    """Redirect."""

    return redirect(reverse("v1:cart", args=[response.result.slug_product]))


def render_finilaze_review(
    request: HttpRequest,
    response: SuccessResponse[DTOResponseFinalizeAPI],
    template: Template,
) -> HttpResponse:
    """Возвращает либо JSON-ответ, либо HTML в зависимости от типа запроса."""
    if request.headers.get("Content-Type") == "application/json":
        return JsonResponse(
            {
                "status": response.status,
                "result": {
                    "carts": response.result.carts,
                    "total_price": response.result.total_price,
                    "form": response.result.form,
                },
            },
        )
    else:
        return render(
            request,
            template,
            {
                "carts": response.result.carts,
                "total_price": response.result.total_price,
                "form": response.result.form,
            },
        )
