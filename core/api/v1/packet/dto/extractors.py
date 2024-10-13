from django.http import HttpRequest

from core.api.v1.packet.dto.base import DTOPacketAPI


def extract_add_packet_dto(
    request: HttpRequest,
) -> DTOPacketAPI:
    product_id = request.POST.get("product_id")

    is_authenticated = request.user.is_authenticated

    username = request.user.username if is_authenticated else None
    session_key = request.session.session_key if is_authenticated else None

    return DTOPacketAPI(
        is_authenticated=is_authenticated,
        username=username,
        product_id=int(product_id),
        session_key=session_key,
    )
