from django.http import (
    HttpRequest,
    HttpResponse,
)
from ninja import Router

from core.api.schemas import SuccessResponse
from core.api.v1.users.dto.base import (
    DTOLoginPageAPI,
    DTORegistrationPageAPI,
)
from core.api.v1.users.dto.extractors import (
    extract_authenticate_dto,
    extract_login_page_dto,
    extract_logout_dto,
    extract_registration_dto,
)
from core.api.v1.users.dto.responses import (
    DTOResponseAuthenticateAPI,
    DTOResponseLoginAPI,
    DTOResponseLogoutPageAPI,
    DTOResponseRegistrationAPI,
)
from core.api.v1.users.renders import (
    render_authenticate,
    render_login,
    render_logout,
    render_registration,
)
from core.apps.users.use_cases.login import (
    AuthenticatePageCommand,
    LoginPageCommand,
)
from core.apps.users.use_cases.logout import LogoutCommand
from core.apps.users.use_cases.registration import RegistrationPageCommand
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


@router.post(
    "login_post",
    url_name="login_post",
)
def login_post(
    request: HttpRequest,
) -> HttpResponse:
    """API: Аутентификации и Авторизации."""
    container = init_container()
    mediator: Mediator = container.resolve(Mediator)

    authenticate_request_dto = extract_authenticate_dto(
        request=request,
    )

    try:
        dto_response_authenticate_api: DTOResponseAuthenticateAPI = (
            mediator.handle_command(
                AuthenticatePageCommand(
                    username=authenticate_request_dto.username,
                    email=authenticate_request_dto.email,
                    password=authenticate_request_dto.password,
                    session_key=authenticate_request_dto.session_key,
                    is_authenticated=authenticate_request_dto.is_authenticated,
                    request=request,
                ),
            )[0]
        )
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.exception},
        )

    return render_authenticate(
        request=request,
        response=SuccessResponse(result=dto_response_authenticate_api),
        template="main_favorite/index.html",
    )


@router.post(
    "logout",
    url_name="logout",
)
def logout(
    request: HttpRequest,
) -> HttpResponse:
    """API: Выход с аккаунта."""
    container = init_container()
    mediator: Mediator = container.resolve(Mediator)

    logout_request_dto = extract_logout_dto(
        request=request,
    )

    try:
        dto_response_logout_api: DTOResponseLogoutPageAPI = mediator.handle_command(
            LogoutCommand(
                username=logout_request_dto.username,
                is_authenticated=logout_request_dto.is_authenticated,
                request=request,
            ),
        )[0]
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.exception},
        )

    return render_logout(
        request=request,
        response=SuccessResponse(result=dto_response_logout_api),
        template="main_favorite/index.html",
    )


@router.get(
    "registration",
    url_name="registration_get",
)
def registration_get(
    request: HttpRequest,
) -> HttpResponse:
    """API: Загрузка странцы Регистрации."""
    container = init_container()
    mediator: Mediator = container.resolve(Mediator)

    registration_page_dto: DTORegistrationPageAPI = extract_registration_dto(
        request=request,
    )

    try:
        dto_response_registration_api: DTOResponseRegistrationAPI = (
            mediator.handle_command(
                RegistrationPageCommand(
                    is_authenticated=registration_page_dto.is_authenticated,
                ),
            )[0]
        )
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.exception},
        )

    return render_registration(
        request=request,
        response=SuccessResponse(result=dto_response_registration_api),
        template="users/registration.html",
    )
