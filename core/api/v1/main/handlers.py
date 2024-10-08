from typing import Optional

from django.http import (
    HttpRequest,
    HttpResponse,
    JsonResponse,
)
from django.shortcuts import render
from ninja import (
    Query,
    Router,
)

from core.api.schemas import SuccessResponse
from core.api.v1.main.dto.extractors import (
    extract_favorite_page_dto,
    extract_main_page_dto,
    extract_save_favorite_dto,
)
from core.api.v1.main.dto.responses import DTOResponseIndexAPI
from core.api.v1.main.renderers import render_index
from core.api.v1.main.schemas import (
    FiltersProductsSchema,
    MainPageResponseSchema,
)
from core.apps.main.use_cases.favorite import FavoritePageCommand
from core.apps.main.use_cases.info import InformationPageCommand
from core.apps.main.use_cases.main import MainPageCommand
from core.apps.main.use_cases.update_favorite import UpdateFavoritePageCommand
from core.infrastructure.di.main import init_container
from core.infrastructure.exceptions.base import BaseAppException
from core.infrastructure.mediator.mediator import Mediator


router = Router(tags=["main"])


@router.get(
    "/index/{category_slug}",
    url_name="index",
    response=MainPageResponseSchema,
)
def index(
    request: HttpRequest,
    filters: Query[FiltersProductsSchema],
    category_slug: Optional[str],
) -> HttpResponse:
    """API: загрузка главной страницы."""
    container = init_container()
    mediator: Mediator = container.resolve(Mediator)

    main_page_dto = extract_main_page_dto(
        request=request,
        filters=filters,
        category_slug=category_slug,
    )

    try:
        dto_response_index_api: DTOResponseIndexAPI = mediator.handle_command(
            MainPageCommand(
                is_authenticated=main_page_dto.is_authenticated,
                username=main_page_dto.username,
                filters=main_page_dto.filters,
                page_number=main_page_dto.page_number,
                category_slug=main_page_dto.category_slug,
            ),
        )[0]
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.message},
        )

    return render_index(
        request=request,
        response=SuccessResponse(result=dto_response_index_api),
        template="main_favorite/index.html",
    )


@router.get(
    "favorites",
    url_name="favorites",
)
def favorites(
    request: HttpRequest,
):
    """API: загрузка страницы с товарами находящимися в избранном."""
    container = init_container()
    mediator: Mediator = container.resolve(Mediator)

    favorite_page_dto = extract_favorite_page_dto(
        request=request,
    )

    try:
        context = mediator.handle_command(
            FavoritePageCommand(
                is_authenticated=favorite_page_dto.is_authenticated,
                username=favorite_page_dto.username,
            ),
        )
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.message},
        )

    return render(request, "main_favorite/favorites.html", context[0])


@router.post(
    "save_favorite",
    url_name="save_favorite",
)
def save_favorite(
    request: HttpRequest,
):
    """API: обновление списка товаров находящихся в избранном."""
    container = init_container()
    mediator: Mediator = container.resolve(Mediator)

    save_favorite_request_dto = extract_save_favorite_dto(
        request=request,
    )

    try:
        mediator.handle_command(
            UpdateFavoritePageCommand(
                is_authenticated=save_favorite_request_dto.is_authenticated,
                product_id=save_favorite_request_dto.product_id,
                username=save_favorite_request_dto.username,
            ),
        )
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.message},
        )

    return JsonResponse({"message": "Данные успешно сохранены"})


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

    return render(request, "main_favorite/information.html", context[0])
