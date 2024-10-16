from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from django.http import HttpRequest
from django.template.loader import render_to_string

from core.api.v1.packet.dto.responses import (
    DTOResponseAddPacketAPI,
    DTOResponseUpdatePacketAPI,
)
from core.apps.common.services.base import BaseQueryGetUserModelService
from core.apps.packet.entities.cart import CartEntity
from core.apps.packet.exceptions.main import DatabaseCartError
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
        # TODO: fix dry
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

        carts_items_user: str = self._render_template(
            packet=updated_packet,
            request=command.request,
        )

        return DTOResponseAddPacketAPI(carts_items_user=carts_items_user)

    @staticmethod
    def _render_template(
        packet: CartEntity,
        request: HttpRequest,
    ) -> str:
        carts_items_user = render_to_string(
            "modal_packet.html",
            {"packet": packet},
            request=request,
        )

        return carts_items_user


@dataclass(frozen=True)
class DeletePacketCommand(BaseCommands):
    cart_id: Optional[int] | None = field(default=None)
    is_profile: Optional[str] | None = field(default=None)
    is_authenticated: bool = field(default=False)
    username: Optional[str] | None = field(default=None)
    session_key: Optional[str] | None = field(default=None)
    request: HttpRequest | None = field(default=None)


@dataclass(frozen=True)
class DeletePacketCommandHandler(CommandHandler[DeletePacketCommand, str]):
    command_delete_cart_from_packet: BaseCommandUpdateDataCartService
    query_get_user_model: BaseQueryGetUserModelService
    query_get_cart_by_user: BaseQueryGetCartService

    def handle(
        self,
        command: DeletePacketCommand,
    ) -> DTOResponseUpdatePacketAPI:
        self.command_delete_cart_from_packet.delete_cart_from_packet(
            cart_id=command.cart_id,
        )

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
        packet, total_quantity = self.query_get_cart_by_user.get_all_carts_by_user(
            filters=filter_kwargs,
        )

        carts_items_user: str = self._render_template(
            is_profile=command.is_profile,
            packet=packet,
            request=command.request,
        )

        return DTOResponseUpdatePacketAPI(
            carts_items_user=carts_items_user,
            new_quantity=total_quantity,
        )

    @staticmethod
    def _render_template(
        is_profile: Optional[str],
        packet: CartEntity,
        request: HttpRequest,
    ) -> str:
        if is_profile == "true":
            carts_items_user = render_to_string(
                "users/packet_profile/packet_profile.html",
                {"packet": packet},
                request=request,
            )
        else:
            carts_items_user = render_to_string(
                "modal_packet.html",
                {"packet": packet},
                request=request,
            )

        return carts_items_user


@dataclass(frozen=True)
class ChangePacketCommand(BaseCommands):
    is_plus: Optional[int] | None = field(default=None)
    cart_id: Optional[int] | None = field(default=None)
    is_profile: Optional[str] | None = field(default=None)
    is_authenticated: bool = field(default=False)
    username: Optional[str] | None = field(default=None)
    session_key: Optional[str] | None = field(default=None)
    request: HttpRequest | None = field(default=None)


@dataclass(frozen=True)
class ChangePacketCommandHandler(CommandHandler[ChangePacketCommand, str]):
    command_change_quantity_cart_from_packet: BaseCommandUpdateDataCartService
    query_get_user_model: BaseQueryGetUserModelService
    query_get_cart: BaseQueryGetCartService

    def handle(
        self,
        command: ChangePacketCommand,
    ) -> DTOResponseUpdatePacketAPI:
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

        cart = self.query_get_cart.get_cart_by_id(cart_id=command.cart_id)
        if not cart:
            raise DatabaseCartError("Not Found Cart")

        self.command_change_quantity_cart_from_packet.process_change_quantity_products_in_packet(
            cart_id=command.cart_id,
            is_plus=command.is_plus,
            cart=cart,
        )

        packet, total_quantity = self.query_get_cart.get_all_carts_by_user(
            filters=filter_kwargs,
        )

        carts_items_user: str = self._render_template(
            is_profile=command.is_profile,
            packet=packet,
            request=command.request,
        )

        return DTOResponseUpdatePacketAPI(
            carts_items_user=carts_items_user,
            new_quantity=total_quantity,
        )

    @staticmethod
    def _render_template(
        is_profile: Optional[str],
        packet: CartEntity,
        request: HttpRequest,
    ) -> str:
        if is_profile == "true":
            carts_items_user = render_to_string(
                "users/packet_profile/packet_profile.html",
                {"packet": packet},
                request=request,
            )
        else:
            carts_items_user = render_to_string(
                "modal_packet.html",
                {"packet": packet},
                request=request,
            )

        return carts_items_user
