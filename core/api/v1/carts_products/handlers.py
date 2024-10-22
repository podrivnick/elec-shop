from typing import Optional

from django.contrib import messages
from django.http import (
    HttpRequest,
    HttpResponse,
)
from ninja import Router

from core.api.schemas import SuccessResponse
from core.api.v1.carts_products.dto.base import (
    DTOCartPageAPI,
    DTOReviewChangeAPI,
    DTOReviewCreateAPI,
    DTOReviewDeleteAPI,
    DTOReviewPageAPI,
)
from core.api.v1.carts_products.dto.extractors import (
    extract_cart_page_dto,
    extract_change_review_dto,
    extract_create_review_dto,
    extract_delete_review_dto,
    extract_reviews_page_dto,
)
from core.api.v1.carts_products.dto.responses import (
    DTOResponseCartAPI,
    DTOResponseChangeReviewAPI,
    DTOResponseCreateReviewAPI,
    DTOResponseDeleteReviewAPI,
    DTOResponseReviewsAPI,
)
from core.api.v1.carts_products.renders import (
    render_cart,
    render_change_review,
    render_create_review,
    render_delete_review,
    render_reviews,
)
from core.apps.carts_products.exceptions.main import UserAlreadyWriteReviewError
from core.apps.carts_products.use_cases.cart import (
    CartPageCommand,
    ReviewsPageCommand,
)
from core.apps.carts_products.use_cases.reviews import (
    ChangeLikesReviewCommand,
    CreateReviewCommand,
    DeleteReviewCommand,
)
from core.infrastructure.di.main import init_container
from core.infrastructure.exceptions.base import BaseAppException
from core.infrastructure.mediator.mediator import Mediator


router = Router(tags=["cart"])


@router.get(
    "/{product}",
    url_name="cart",
)
def cart(
    request: HttpRequest,
    product: Optional[str],
) -> HttpResponse:
    """API: Загрузка страницы товара."""
    container = init_container()
    mediator: Mediator = container.resolve(Mediator)

    cart_page_dto: DTOCartPageAPI = extract_cart_page_dto(
        request=request,
        product=product,
    )

    try:
        dto_response_cart_api: DTOResponseCartAPI = mediator.handle_command(
            CartPageCommand(
                is_authenticated=cart_page_dto.is_authenticated,
                username=cart_page_dto.username,
                product_slug=cart_page_dto.product_slug,
            ),
        )[0]
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.message},
        )

    return render_cart(
        request=request,
        response=SuccessResponse(result=dto_response_cart_api),
        template="carts_products/cart_product.html",
    )


@router.get(
    "/reviews/{product}",
    url_name="reviews",
)
def reviews(
    request: HttpRequest,
    product: Optional[str],
) -> HttpResponse:
    """API: Загрузка страницы отзывов к товару."""
    container = init_container()
    mediator: Mediator = container.resolve(Mediator)

    reviews_page_dto: DTOReviewPageAPI = extract_reviews_page_dto(
        request=request,
        product=product,
    )

    try:
        dto_response_reviews_api: DTOResponseReviewsAPI = mediator.handle_command(
            ReviewsPageCommand(
                is_authenticated=reviews_page_dto.is_authenticated,
                username=reviews_page_dto.username,
                product_slug=reviews_page_dto.product_slug,
            ),
        )[0]
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.message},
        )

    return render_reviews(
        request=request,
        response=SuccessResponse(result=dto_response_reviews_api),
        template="carts_products/all_opinions.html",
    )


@router.post(
    "/reviews/create_review/",
    url_name="reviews_create",
)
def reviews_create(
    request: HttpRequest,
) -> HttpResponse:
    """API: Создание отзыва."""
    container = init_container()
    mediator: Mediator = container.resolve(Mediator)

    reviews_create_dto: DTOReviewCreateAPI = extract_create_review_dto(
        request=request,
    )

    try:
        dto_response_reviews_create_api: DTOResponseCreateReviewAPI = (
            mediator.handle_command(
                CreateReviewCommand(
                    is_authenticated=reviews_create_dto.is_authenticated,
                    username=reviews_create_dto.username,
                    review=reviews_create_dto.review,
                    id_product=reviews_create_dto.id_product,
                    product_slug=reviews_create_dto.product_slug,
                ),
            )[0]
        )
    except UserAlreadyWriteReviewError as e:
        messages.success(
            request,
            e.message,
        )
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.message},
        )

    return render_create_review(
        request=request,
        response=SuccessResponse(result=dto_response_reviews_create_api),
    )


@router.post(
    "/reviews/change_like/",
    url_name="change_like",
)
def change_like(
    request: HttpRequest,
) -> HttpResponse:
    """API: Изменение количества лайков."""
    container = init_container()
    mediator: Mediator = container.resolve(Mediator)

    reviews_change_dto: DTOReviewChangeAPI = extract_change_review_dto(
        request=request,
    )

    try:
        dto_response_reviews_change_likes_api: DTOResponseChangeReviewAPI = (
            mediator.handle_command(
                ChangeLikesReviewCommand(
                    is_authenticated=reviews_change_dto.is_authenticated,
                    username=reviews_change_dto.username,
                    product_id=reviews_change_dto.product_id,
                    review_id=reviews_change_dto.review_id,
                ),
            )[0]
        )
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.message},
        )

    return render_change_review(
        request=request,
        response=SuccessResponse(result=dto_response_reviews_change_likes_api),
    )


@router.post(
    "/reviews/delete_reveiw/",
    url_name="delete_reveiw",
)
def delete_reveiw(
    request: HttpRequest,
) -> HttpResponse:
    """API: Удаление отзывов."""
    container = init_container()
    mediator: Mediator = container.resolve(Mediator)

    reviews_delete_dto: DTOReviewDeleteAPI = extract_delete_review_dto(
        request=request,
    )

    try:
        dto_response_delete_review_api: DTOResponseDeleteReviewAPI = (
            mediator.handle_command(
                DeleteReviewCommand(
                    is_authenticated=reviews_delete_dto.is_authenticated,
                    username=reviews_delete_dto.username,
                    slug_product=reviews_delete_dto.slug_product,
                    pk_product=reviews_delete_dto.pk_product,
                ),
            )[0]
        )
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.message},
        )

    return render_delete_review(
        request=request,
        response=SuccessResponse(result=dto_response_delete_review_api),
    )
