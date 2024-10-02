from django.http import HttpRequest

from ninja import Router

from core.api.schemas import ApiResponse
from core.api.v1.customers.schemas import (
    AuthInSchema,
    AuthOutSchema,
)
from core.apps.customers.services.auth import BaseAuthService
from core.project.containers import get_container


router = Router(tags=["Customers"])


@router.get("index", response=ApiResponse[AuthOutSchema], operation_id="authorize")
def main_handler(
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
