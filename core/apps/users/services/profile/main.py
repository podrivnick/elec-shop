from dataclasses import dataclass
from typing import List

from core.apps.packet.entities.cart import CartEntity
from core.apps.packet.models import Cart
from core.apps.users import value_objects as vo
from core.apps.users.services.profile.base import BaseQueryFilterCartsByUserService


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
