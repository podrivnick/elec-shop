from django.http import HttpRequest

from ninja import (
    Query,
    Router,
)

from core.api.filters import PaginationIn
from core.api.v1.main.schemas import FiltersProductsSchema
from core.apps.customers.services.auth import BaseAuthService
from core.infrastructure.di.main import init_container
from core.infrastructure.exceptions.base import BaseAppException
from core.infrastructure.mediator.mediator import Mediator
from core.project.containers import get_container


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
    """Загрузка главной страницы."""
    container = init_container()

    mediator: Mediator = container.resolve(Mediator)

    try:
        flower = await mediator.handle_command()
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.message},
        )

    return flower


@router.get("favorites", response=ApiResponse[AuthOutSchema], operation_id="authorize")
def favorite_handler(
    request: HttpRequest,
    schema: AuthInSchema,
) -> ApiResponse[AuthOutSchema]:
    container = get_container()
    service = container.resolve(BaseAuthService)

    service.authorize(schema.phone)

    return ApiResponse(
        data=AuthOutSchema(
            message=f"Code is sent to: {schema.phone}",
        ),
    )


@router.post(
    "update_favorite",
    response=ApiResponse[AuthOutSchema],
    operation_id="authorize",
)
def update_favorite_handler(
    request: HttpRequest,
    schema: AuthInSchema,
) -> ApiResponse[AuthOutSchema]:
    container = get_container()
    service = container.resolve(BaseAuthService)

    service.authorize(schema.phone)

    return ApiResponse(
        data=AuthOutSchema(
            message=f"Code is sent to: {schema.phone}",
        ),
    )


@router.get("faq", response=ApiResponse[AuthOutSchema], operation_id="informatio")
def faq_handler(
    request: HttpRequest,
    schema: AuthInSchema,
) -> ApiResponse[AuthOutSchema]:
    container = get_container()
    service = container.resolve(BaseAuthService)

    service.authorize(schema.phone)

    return ApiResponse(
        data=AuthOutSchema(
            message=f"Code is sent to: {schema.phone}",
        ),
    )
