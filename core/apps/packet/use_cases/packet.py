from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from django.http import HttpRequest
from django.template.loader import render_to_string

from core.api.v1.packet.dto.responses import DTOResponseAddPacketAPI
from core.apps.common.services.base import BaseQueryGetUserModelService
from core.apps.packet.services.base import (
    BaseCommandUpdateDataCartService,
    BaseQueryGetCartService,
    BaseQueryGetProductService,
)
from core.apps.users import value_objects as vo
from core.infrastructure.mediator.base import BaseCommands
from core.infrastructure.mediator.handlers.commands import CommandHandler


@dataclass(frozen=True)
class AddPacketCommand(BaseCommands):
    is_authenticated: bool = field(default=False)
    username: Optional[str] | None = field(default=None)
    product_id: Optional[int] | None = field(default=None)
    session_key: Optional[str] | None = field(default=None)
    request: HttpRequest | None = field(default=None)


@dataclass(frozen=True)
class AddPacketCommandHandler(CommandHandler[AddPacketCommand, str]):
    query_get_user_model: BaseQueryGetUserModelService
    query_get_product_by_id: BaseQueryGetProductService
    query_get_cart_by_product_and_user: BaseQueryGetCartService
    command_update_or_create_cart: BaseCommandUpdateDataCartService

    def handle(
        self,
        command: AddPacketCommand,
    ) -> DTOResponseAddPacketAPI:
        if command.is_authenticated:
            username = vo.UserName(command.username)
            user = self.query_get_user_model.get_usermodel_by_username(
                username=username.to_raw(),
            )

        filter_kwargs = (
            {"user": user}
            if command.is_authenticated
            else {"session_key": command.session_key}
        )

        product = self.query_get_product_by_id.get_product_by_id(
            id_product=command.product_id,
        )
        packet = self.query_get_cart_by_product_and_user.get_cart_by_product_and_user(
            product=product,
            filters=filter_kwargs,
        )

        updated_packet = self.command_update_or_create_cart.update_or_create_cart(
            product=product,
            packet=packet,
            filters=filter_kwargs,
        )

        carts_items_user = render_to_string(
            "modal_packet.html",
            {"packet": updated_packet},
            request=command.request,
        )

        return DTOResponseAddPacketAPI(carts_items_user=carts_items_user)
