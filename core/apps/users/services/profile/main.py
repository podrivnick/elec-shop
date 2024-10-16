from dataclasses import dataclass
from typing import (
    Dict,
    List,
)

from django.db import transaction
from django.db.models import QuerySet

from core.apps.packet.entities.cart import CartEntity
from core.apps.packet.models.cart import Cart
from core.apps.users import value_objects as vo
from core.apps.users.entities.user import User as UserEntity
from core.apps.users.models import User
from core.apps.users.services.profile.base import (
    BaseCommandSetUpdatedInformationOfUserService,
    BaseQueryFilterCartsByUserService,
    BaseQueryValidateNewDataService,
)


@dataclass
class ORMQueryFilterCartsByUserService(BaseQueryFilterCartsByUserService):
    def get_carts_user(
        self,
        username: vo.UserName,
    ) -> List[CartEntity]:
        carts = Cart.objects.filter(user__username=username.to_raw()).order_by(
            "-quantity",
        )
        list_carts = [cart.to_entity() for cart in carts]

        return list_carts


@dataclass
class QueryValidateNewDataService(BaseQueryValidateNewDataService):
    def validate_new_information_user(
        self,
        user: QuerySet[User],
        new_data: UserEntity,
    ) -> Dict:
        updated_fields = {}

        for par, value in new_data.to_dict().items():
            current_value_in_user = getattr(user, par, None)
            if value and value.to_raw() != current_value_in_user:
                updated_fields[par] = value.to_raw()

        return updated_fields or None


@dataclass
class ORMCommandSetUpdatedInformationOfUserService(
    BaseCommandSetUpdatedInformationOfUserService,
):
    def set_information_user(
        self,
        user: QuerySet[User],
        updated_information: Dict,
    ):
        with transaction.atomic():
            for field, value in updated_information.items():
                if value is not None:
                    setattr(user, field, value)

            user.save(update_fields=updated_information.keys())
