from dataclasses import (
    dataclass,
    field,
)
from typing import Optional

from core.api.v1.orders.dto.responses import DTOResponseOrderAPI
from core.apps.common.exceptions.main import AuthenticationError
from core.apps.common.services.base import BaseQueryGetUserModelService
from core.apps.orders.exceptions.order import OrderNotCreatedError
from core.apps.orders.repositories.base import BaseCommandOrderRepository
from core.apps.orders.services.base import (
    BaseCommandOrderService,
    BaseQueryValidationOrderService,
)
from core.apps.packet.services.base import BaseQueryGetCartService
from core.infrastructure.mediator.base import BaseCommands
from core.infrastructure.mediator.handlers.commands import CommandHandler


@dataclass(frozen=True)
class OrderCommand(BaseCommands):
    is_authenticated: bool = field(default=False)
    username: Optional[str] | None = field(default=None)
    first_name: Optional[str] | None = field(default=None)
    last_name: Optional[str] | None = field(default=None)
    email: Optional[str] | None = field(default=None)
    phone: Optional[str] | None = field(default=None)
    delivery_address: Optional[str] | None = field(default=None)
    required_delivery: Optional[str] | None = field(default=None)
    payment_on_get: Optional[str] | None = field(default=None)
    total_price: Optional[str] | None = field(default=None)


@dataclass(frozen=True)
class OrderCommandHandler(CommandHandler[OrderCommand, str]):
    query_get_user_model_by_username: BaseQueryGetUserModelService
    query_validation_order_data_service: BaseQueryValidationOrderService  # TODO
    command_create_basic_order: BaseCommandOrderService
    query_filter_packet_service: BaseQueryGetCartService
    command_order_repository: BaseCommandOrderRepository

    def handle(
        self,
        command: OrderCommand,
    ) -> DTOResponseOrderAPI:
        if not command.is_authenticated:
            raise AuthenticationError("User is not authenticated.")

        user = self.query_get_user_model_by_username.get_usermodel_by_username(
            username=command.username,
        )

        order_entity = self.query_validation_order_data_service.validate_order_data(
            first_name=command.first_name,
            last_name=command.last_name,
            email=command.email,
            phone=command.phone,
            delivery_address=command.delivery_address,
            required_delivery=command.required_delivery,
            payment_on_get=command.payment_on_get,
            total_price=command.total_price,
        )

        basic_order = self.command_create_basic_order.create_basic_order(
            user=user,
            order=order_entity,
        )

        carts = self.query_filter_packet_service.get_carts_by_user_quantity(user=user)

        try:
            self.command_create_basic_order.create_orders_items(
                basic_order=basic_order,
                carts=carts,
            )
        except Exception as e:
            self.command_order_repository.delete_basic_order(
                order=basic_order,
            )

            raise OrderNotCreatedError(e)

        return DTOResponseOrderAPI(
            username=command.username,
        )
