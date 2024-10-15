from django.http import (
    HttpRequest,
    HttpResponse,
)
from ninja import Router

from core.api.schemas import SuccessResponse
from core.api.v1.packet.dto.base import (
    DTOChangePacketAPI,
    DTODeletePacketAPI,
    DTOPacketAPI,
)
from core.api.v1.packet.dto.extractors import (
    extract_add_packet_dto,
    extract_change_packet_dto,
    extract_delete_packet_dto,
)
from core.api.v1.packet.dto.responses import (
    DTOResponseAddPacketAPI,
    DTOResponseUpdatePacketAPI,
)
from core.api.v1.packet.renders import (
    render_add_packet,
    render_change_packet,
    render_delete_packet,
)
from core.apps.packet.use_cases.packet import (
    AddPacketCommand,
    ChangePacketCommand,
    DeletePacketCommand,
)
from core.infrastructure.di.main import init_container
from core.infrastructure.exceptions.base import BaseAppException
from core.infrastructure.mediator.mediator import Mediator


router = Router(tags=["packet"])


@router.post(
    "add_packet",
    url_name="add_packet",
)
def add_packet(
    request: HttpRequest,
) -> HttpResponse:
    """API: Добавление Товаров в Корзину."""
    container = init_container()
    mediator: Mediator = container.resolve(Mediator)

    add_packet_request_dto: DTOPacketAPI = extract_add_packet_dto(
        request=request,
    )

    try:
        dto_response_add_packet_api: DTOResponseAddPacketAPI = mediator.handle_command(
            AddPacketCommand(
                username=add_packet_request_dto.username,
                session_key=add_packet_request_dto.session_key,
                is_authenticated=add_packet_request_dto.is_authenticated,
                product_id=add_packet_request_dto.product_id,
                request=request,
            ),
        )[0]
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.exception},
        )

    return render_add_packet(
        request=request,
        response=SuccessResponse(result=dto_response_add_packet_api),
        template="modal_packet.html",
    )


@router.post(
    "delete_packet",
    url_name="delete_packet",
)
def delete_packet(
    request: HttpRequest,
) -> HttpResponse:
    """API: Удаление Товаров с Корзины."""
    container = init_container()
    mediator: Mediator = container.resolve(Mediator)

    delete_packet_request_dto: DTODeletePacketAPI = extract_delete_packet_dto(
        request=request,
    )

    try:
        dto_response_delete_packet_api: DTOResponseUpdatePacketAPI = (
            mediator.handle_command(
                DeletePacketCommand(
                    cart_id=delete_packet_request_dto.cart_id,
                    is_profile=delete_packet_request_dto.is_profile,
                    is_authenticated=delete_packet_request_dto.is_authenticated,
                    username=delete_packet_request_dto.username,
                    session_key=delete_packet_request_dto.session_key,
                    request=request,
                ),
            )[0]
        )
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.exception},
        )

    return render_delete_packet(
        request=request,
        response=SuccessResponse(result=dto_response_delete_packet_api),
    )


@router.post(
    "change_packet",
    url_name="change_packet",
)
def change_packet(
    request: HttpRequest,
) -> HttpResponse:
    """API: Изменение Количества Товаров в Корзине."""
    container = init_container()
    mediator: Mediator = container.resolve(Mediator)

    change_packet_request_dto: DTOChangePacketAPI = extract_change_packet_dto(
        request=request,
    )

    try:
        dto_response_change_packet_api: DTOResponseUpdatePacketAPI = (
            mediator.handle_command(
                ChangePacketCommand(
                    is_plus=change_packet_request_dto.is_plus,
                    cart_id=change_packet_request_dto.cart_id,
                    is_profile=change_packet_request_dto.is_profile,
                    is_authenticated=change_packet_request_dto.is_authenticated,
                    username=change_packet_request_dto.username,
                    session_key=change_packet_request_dto.session_key,
                    request=request,
                ),
            )[0]
        )
    except BaseAppException as exception:
        raise ValueError(
            detail={"error": exception.exception},
        )

    return render_change_packet(
        request=request,
        response=SuccessResponse(result=dto_response_change_packet_api),
        template="main_favorite/index.html",
    )
