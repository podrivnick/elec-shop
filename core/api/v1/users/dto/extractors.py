from django.http import HttpRequest

from core.api.v1.users.dto.base import DTOLoginPageAPI


def extract_login_page_dto(
    request: HttpRequest,
) -> DTOLoginPageAPI:
    is_authenticated = request.user.is_authenticated
    username = request.user.username if is_authenticated else None

    return DTOLoginPageAPI(
        is_authenticated=is_authenticated,
        username=username,
    )
