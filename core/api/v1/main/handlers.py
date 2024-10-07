from typing import Optional

from django.http import HttpRequest
from django.shortcuts import render

from ninja import (
    Query,
    Router,
)

from core.api.v1.main.schemas import (
    FiltersProductsSchema,
    MainPageResponseSchema,
    ProductIdSchema,
)
from core.apps.main.use_cases.favorite import FavoritePageCommand
from core.apps.main.use_cases.info import InformationPageCommand
from core.apps.main.use_cases.main import MainPageCommand
from core.apps.main.use_cases.update_favorite import UpdateFavoritePageCommand
from core.infrastructure.di.main import init_container
from core.infrastructure.exceptions.base import BaseAppException
from core.infrastructure.mediator.mediator import Mediator


router = Router(tags=["main"])


class ApiResponse:
    pass


@router.get(
    "/index/{category_slug}",
    url_name="index",
    response=MainPageResponseSchema,
)
def index(
    request: HttpRequest,
    filters: Query[FiltersProductsSchema],
    category_slug: Optional[str],
):
    """API: загрузка главной страницы."""
    container = init_container()
    mediator: Mediator = container.resolve(Mediator)

    page_number = request.GET.get("page")
    is_authenticated = request.user.is_authenticated

    try:
        context = mediator.handle_command(
            MainPageCommand(
                is_authenticated=is_authenticated,
                username=request.user.username,
                filters=filters,
                page_number=page_number,
                category_slug=category_slug,
            ),
        )
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.message},
        )

    return render(request, "main_favorite/index.html", context[0])


@router.get("favorites", url_name="favorites")
def favorites(
    request: HttpRequest,
):
    """API: загрузка страницы с товарами находящимися в избранном."""
    container = init_container()

    mediator: Mediator = container.resolve(Mediator)

    try:
        context = mediator.handle_command(
            FavoritePageCommand(),
        )
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.message},
        )

    return render(request, "main_favorite/favorites.html", context)


@router.post(
    "save_favorite",
    url_name="save_favorite",
)
def save_favorite(
    request: HttpRequest,
    product_id: ProductIdSchema,
):
    """API: обновление списка товаров находящихся в избранном."""
    container = init_container()

    mediator: Mediator = container.resolve(Mediator)

    try:
        context = mediator.handle_command(
            UpdateFavoritePageCommand(),
        )
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.message},
        )

    return ApiResponse(context)


@router.get("information", url_name="information")
def information(
    request: HttpRequest,
):
    """API: загрузка страницы с общей информацией."""
    container = init_container()

    mediator: Mediator = container.resolve(Mediator)

    try:
        context = mediator.handle_command(
            InformationPageCommand(),
        )
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.message},
        )

    return render(request, "main_favorite/information.html", context)
