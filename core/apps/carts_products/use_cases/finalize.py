from dataclasses import (
    dataclass,
    field,
)
from typing import (
    List,
    Optional,
)

from django.db.models import QuerySet

from core.api.v1.carts_products.dto.responses import DTOResponseFinalizeAPI
from core.apps.common.exceptions.main import AuthenticationError
from core.apps.common.services.base import BaseQueryGetUserModelService
from core.apps.orders.schemas.main import OrderSchema
from core.apps.packet.entities.cart import CartEntity
from core.apps.packet.services.base import BaseQueryGetCartService
from core.apps.users.models import User
from core.infrastructure.mediator.base import BaseCommands
from core.infrastructure.mediator.handlers.commands import CommandHandler


@dataclass(frozen=True)
class FinalizePageCommand(BaseCommands):
    is_authenticated: bool = field(default=False)
    username: Optional[str] | None = field(default=None)


@dataclass(frozen=True)
class FinalizePageCommandHandler(CommandHandler[FinalizePageCommand, str]):
    query_get_user_model_by_username: BaseQueryGetUserModelService
    query_get_carts_service: BaseQueryGetCartService

    def handle(
        self,
        command: FinalizePageCommand,
    ) -> DTOResponseFinalizeAPI:
        if not command.is_authenticated:
            raise AuthenticationError("User is not authenticated.")
        user = self.query_get_user_model_by_username.get_usermodel_by_username(
            username=command.username,
        )

        carts = self.query_get_carts_service.get_all_carts_by_user(
            filters={
                "user": user,
            },
        )[0]

        total_price = self.total_price_carts(carts=carts)
        form = self.formating_data_of_user_to_form(user=user)

        return DTOResponseFinalizeAPI(
            carts=carts,
            total_price=total_price,
            form=form,
        )

    @staticmethod
    def total_price_carts(carts: List[CartEntity]) -> int:
        return sum(cart.products_price for cart in carts)

    @staticmethod
    def formating_data_of_user_to_form(user: QuerySet[User]) -> OrderSchema:
        initial_data = {}
        data_form_finalize = {
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "email",
            "phone": "phone",
        }

        for key, value in data_form_finalize.items():
            if not hasattr(user, value):
                continue

            attribute_value = getattr(user, value)

            if attribute_value is None:
                continue

            initial_data[key] = attribute_value

        order_form = OrderSchema(**initial_data)

        return order_form
