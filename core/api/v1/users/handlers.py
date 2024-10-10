from django.http import (
    HttpRequest,
    HttpResponse,
    JsonResponse,
)
from ninja import Router

from core.api.schemas import SuccessResponse
from core.api.v1.main.dto.extractors import extract_save_favorite_dto
from core.api.v1.main.dto.responses import DTOResponseFavoriteAPI
from core.api.v1.main.renders import (
    render_favorites,
    render_update_favorite,
)
from core.api.v1.users.dto.base import DTOLoginPageAPI
from core.api.v1.users.dto.extractors import extract_login_page_dto
from core.apps.main.use_cases.favorite import FavoritePageCommand
from core.apps.main.use_cases.update_favorite import UpdateFavoritePageCommand
from core.infrastructure.di.main import init_container
from core.infrastructure.exceptions.base import BaseAppException
from core.infrastructure.mediator.mediator import Mediator


router = Router(tags=["user"])


@router.get(
    "login",
    url_name="login",
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
        dto_response_login_api: DTOResponseFavoriteAPI = mediator.handle_command(
            FavoritePageCommand(
                is_authenticated=login_page_dto.is_authenticated,
                username=login_page_dto.username,
            ),
        )[0]
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.message},
        )

    return render_favorites(
        request=request,
        response=SuccessResponse(result=dto_response_login_api),
        template="users/login.html",
    )


@router.post(
    "login_post",
    url_name="login_post",
)
def login_post(
    request: HttpRequest,
) -> JsonResponse:
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

    return render_update_favorite(
        request=request,
        response=SuccessResponse(result="Данные успешно сохранены"),
    )
