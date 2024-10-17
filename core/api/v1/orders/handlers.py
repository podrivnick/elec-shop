from typing import Optional

from django.http import (
    HttpRequest,
    HttpResponse,
)
from ninja import (
    Query,
    Router,
)

from core.api.schemas import SuccessResponse
from core.api.v1.main.dto.extractors import extract_main_page_dto
from core.api.v1.main.dto.responses import DTOResponseIndexAPI
from core.api.v1.main.renders import render_index
from core.api.v1.main.schemas import (
    FiltersProductsSchema,
    MainPageResponseSchema,
)
from core.apps.main.use_cases.main import MainPageCommand
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
