from django.http import HttpRequest

from core.api.v1.users.dto.base import (
    DTOAuthenticateAPI,
    DTOLoginPageAPI,
    DTOLogoutPageAPI,
    DTOProifleAPI,
    DTORegisterAPI,
    DTORegistrationPageAPI,
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


def extract_registration_dto(
    request: HttpRequest,
) -> DTORegistrationPageAPI:
    is_authenticated = request.user.is_authenticated
    username = request.user.username if is_authenticated else None

    return DTORegistrationPageAPI(
        username=username,
        is_authenticated=is_authenticated,
    )


def extract_register_dto(
    request: HttpRequest,
) -> DTORegisterAPI:
    is_authenticated = request.user.is_authenticated
    first_name = request.POST.get("first_name", "")
    last_name = request.POST.get("last_name", "")
    username = request.POST.get("username", "")
    email = request.POST.get("email", "")
    password1 = request.POST.get("password1", "")
    password2 = request.POST.get("password2", "")
    session_key = request.session.session_key or False

    return DTORegisterAPI(
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        password1=password1,
        password2=password2,
        session_key=session_key,
        is_authenticated=is_authenticated,
    )


def extract_profile_dto(
    request: HttpRequest,
) -> DTOProifleAPI:
    is_authenticated = request.user.is_authenticated
    username = request.user.username if is_authenticated else None
    user = request.user

    updated_information = request.GET.dict() or None
    referer = request.META.get("HTTP_REFERER") if updated_information else None

    return DTOProifleAPI(
        username=username,
        referer=referer,
        is_authenticated=is_authenticated,
        user=user,
        updated_information=updated_information,
    )
