from django.http import HttpRequest
from django.shortcuts import render

from ninja import (
    Query,
    Router,
)

from core.api.filters import PaginationIn
from core.api.v1.main.schemas import FiltersProductsSchema
from core.apps.main.use_cases.favorite import FavoritePageCommand
from core.apps.main.use_cases.info import InformationPageCommand
from core.apps.main.use_cases.main import MainPageCommand
from core.apps.main.use_cases.update_favorite import UpdateFavoritePageCommand
from core.infrastructure.di.main import init_container
from core.infrastructure.exceptions.base import BaseAppException
from core.infrastructure.mediator.mediator import Mediator


router = Router(tags=["Main Page"])


class ApiResponse:
    pass


class AuthOutSchema:
    pass


class AuthInSchema:
    pass


@router.get("index", response=ApiResponse[AuthOutSchema], operation_id="main")
def main_handler(
    request: HttpRequest,
    schema: FiltersProductsSchema,
    pagination_in: Query[PaginationIn],
) -> ApiResponse[AuthOutSchema]:
    """API: загрузка главной страницы."""
    container = init_container()

    mediator: Mediator = container.resolve(Mediator)

    try:
        context = await mediator.handle_command(
            MainPageCommand(),
        )
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.message},
        )

    return render(request, "main_favorite/index.html", context)


@router.get("favorites", response=ApiResponse[AuthOutSchema], operation_id="authorize")
def favorite_handler(
    request: HttpRequest,
    schema: AuthInSchema,
) -> ApiResponse[AuthOutSchema]:
    """API: загрузка страницы с товарами находящимися в избранном."""
    container = init_container()

    mediator: Mediator = container.resolve(Mediator)

    try:
        context = await mediator.handle_command(
            FavoritePageCommand(),
        )
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.message},
        )

    return render(request, "main_favorite/favorites.html", context)


@router.post(
    "update_favorite",
    response=ApiResponse[AuthOutSchema],
    operation_id="authorize",
)
def update_favorite_handler(
    request: HttpRequest,
    schema: AuthInSchema,
) -> ApiResponse[AuthOutSchema]:
    """API: обновление списка товаров находящихся в избранном."""
    container = init_container()

    mediator: Mediator = container.resolve(Mediator)

    try:
        context = await mediator.handle_command(
            UpdateFavoritePageCommand(),
        )
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.message},
        )

    return ApiResponse(context)


@router.get("faq", response=ApiResponse[AuthOutSchema], operation_id="informatio")
def faq_handler(
    request: HttpRequest,
    schema: AuthInSchema,
) -> ApiResponse[AuthOutSchema]:
    """API: загрузка страницы с общей информацией."""
    container = init_container()

    mediator: Mediator = container.resolve(Mediator)

    try:
        context = await mediator.handle_command(
            InformationPageCommand(),
        )
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.message},
        )

    return render(request, "main_favorite/information.html", context)
