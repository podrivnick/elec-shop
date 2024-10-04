from django.http import HttpRequest
from django.shortcuts import render

from ninja import (
    Query,
    Router,
)

from core.api.filters import PaginationIn
from core.api.v1.main.schemas import (
    FiltersProductsSchema,
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


class AuthOutSchema:
    pass


class AuthInSchema:
    pass


@router.get("index", operation_id="index")
def main_handler(
    request: HttpRequest,
    schema: FiltersProductsSchema,
    pagination_in: Query[PaginationIn],
):
    """API: загрузка главной страницы."""
    container = init_container()

    mediator: Mediator = container.resolve(Mediator)

    try:
        context = mediator.handle_command(
            MainPageCommand(),
        )
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.message},
        )

    return render(request, "main_favorite/index.html", context)


@router.get("favorites", operation_id="favorites")
def favorite_handler(
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
    operation_id="save_favorite",
)
def update_favorite_handler(
    request: HttpRequest,
    schema: ProductIdSchema,
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


@router.get("information", operation_id="information")
def faq_handler(
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
