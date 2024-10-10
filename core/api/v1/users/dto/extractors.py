from django.http import HttpRequest

from core.api.v1.users.dto.base import (
    DTOAuthenticateAPI,
    DTOLoginPageAPI,
    DTOLogoutPageAPI,
)


def extract_login_page_dto(
    request: HttpRequest,
) -> DTOLoginPageAPI:
    is_authenticated = request.user.is_authenticated
    username = request.user.username if is_authenticated else None

    return DTOLoginPageAPI(
        is_authenticated=is_authenticated,
        username=username,
    )


def extract_authenticate_dto(
    request: HttpRequest,
) -> DTOAuthenticateAPI:
    is_authenticated = request.user.is_authenticated
    username = request.POST.get("username", "")
    email = request.POST.get("email", "")
    password = request.POST.get("password", "")
    session_key = request.session.session_key or False

    return DTOAuthenticateAPI(
        username=username,
        email=email,
        password=password,
        is_authenticated=is_authenticated,
        session_key=session_key,
    )


def extract_logout_dto(
    request: HttpRequest,
) -> DTOLogoutPageAPI:
    is_authenticated = request.user.is_authenticated
    username = request.POST.get("username", "")

    return DTOLogoutPageAPI(
        username=username,
        is_authenticated=is_authenticated,
    )
