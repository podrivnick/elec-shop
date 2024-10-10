from django.http import (
    HttpRequest,
    HttpResponse,
)
from ninja import Router

from core.api.schemas import SuccessResponse
from core.api.v1.users.dto.base import DTOLoginPageAPI
from core.api.v1.users.dto.extractors import extract_login_page_dto
from core.api.v1.users.dto.responses import DTOResponseLoginAPI
from core.api.v1.users.renders import render_login
from core.apps.users.use_cases.login import LoginPageCommand
from core.infrastructure.di.main import init_container
from core.infrastructure.exceptions.base import BaseAppException
from core.infrastructure.mediator.mediator import Mediator


router = Router(tags=["user"])


@router.get(
    "login",
    url_name="login_get",
)
def login_get(
    request: HttpRequest,
) -> HttpResponse:
    """API: Загрузка странцы Авторизации."""
    container = init_container()
    mediator: Mediator = container.resolve(Mediator)

    login_page_dto: DTOLoginPageAPI = extract_login_page_dto(
        request=request,
    )

    try:
        dto_response_login_api: DTOResponseLoginAPI = mediator.handle_command(
            LoginPageCommand(
                is_authenticated=login_page_dto.is_authenticated,
            ),
        )[0]
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.message},
        )

    return render_login(
        request=request,
        response=SuccessResponse(result=dto_response_login_api),
        template="users/login.html",
    )


# @router.post(
#     "login_post",
#     url_name="login_post",
# )
# def login_post(
#     request: HttpRequest,
# ) -> JsonResponse:
#     """API: обновление списка товаров находящихся в избранном."""
#     container = init_container()
#     mediator: Mediator = container.resolve(Mediator)

#     save_favorite_request_dto = extract_save_favorite_dto(
#         request=request,
#     )

#     try:
#         mediator.handle_command(
#             UpdateFavoritePageCommand(
#                 is_authenticated=save_favorite_request_dto.is_authenticated,
#                 product_id=save_favorite_request_dto.product_id,
#                 username=save_favorite_request_dto.username,
#             ),
#         )
#     except BaseAppException as exception:
#         raise ValueError(
#             detail={"error": exception.message},
#         )

#     return render_update_favorite(
#         request=request,
#         response=SuccessResponse(result="Данные успешно сохранены"),
#     )
