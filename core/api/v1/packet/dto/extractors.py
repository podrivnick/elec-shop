from django.http import HttpRequest

from core.api.v1.packet.dto.base import (
    DTOChangePacketAPI,
    DTODeletePacketAPI,
    DTOPacketAPI,
)


def extract_add_packet_dto(
    request: HttpRequest,
) -> DTOPacketAPI:
    product_id = request.POST.get("product_id")

    is_authenticated = request.user.is_authenticated

    username = request.user.username if is_authenticated else None
    session_key = request.session.session_key if not is_authenticated else None

    return DTOPacketAPI(
        is_authenticated=is_authenticated,
        username=username,
        product_id=product_id,
        session_key=session_key,
    )


def extract_delete_packet_dto(
    request: HttpRequest,
) -> DTODeletePacketAPI:
    cart_id = request.POST.get("cart_id")
    is_profile = request.POST.get("is_profile")

    is_authenticated = request.user.is_authenticated

    username = request.user.username if is_authenticated else None
    session_key = request.session.session_key if not is_authenticated else None

    return DTODeletePacketAPI(
        cart_id=cart_id,
        is_profile=is_profile,
        is_authenticated=is_authenticated,
        username=username,
        session_key=session_key,
    )


def extract_change_packet_dto(
    request: HttpRequest,
) -> DTOChangePacketAPI:
    is_plus = request.POST.get("is_plus")
    cart_id = request.POST.get("cart_id")
    is_profile = request.POST.get("is_profile")

    is_authenticated = request.user.is_authenticated

    username = request.user.username if is_authenticated else None
    session_key = request.session.session_key if not is_authenticated else None

    return DTOChangePacketAPI(
        is_plus=is_plus,
        cart_id=cart_id,
        is_profile=is_profile,
        is_authenticated=is_authenticated,
        username=username,
        session_key=session_key,
    )
