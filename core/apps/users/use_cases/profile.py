from dataclasses import (
    dataclass,
    field,
)
from typing import (
    List,
    Optional,
)

from django.utils.functional import SimpleLazyObject

from core.api.v1.users.dto.responses import DTOResponseProfileAPI
from core.apps.common.exceptions.main import AuthenticationError
from core.apps.packet.entities.cart import CartEntity
from core.apps.users import value_objects as vo
from core.apps.users.schemas.user_profile import ProfileDataSchema
from core.apps.users.services.profile.base import BaseQueryFilterCartsByUserService
from core.infrastructure.mediator.base import BaseCommands
from core.infrastructure.mediator.handlers.commands import CommandHandler


@dataclass(frozen=True)
class ProfilePageCommand(BaseCommands):
    user: SimpleLazyObject
    is_authenticated: bool = field(default=False)
    referer: Optional[str] | None = field(default=None)
    username: Optional[str] | None = field(default=None)


@dataclass(frozen=True)
class ProfilePageCommandHandler(CommandHandler[ProfilePageCommand, str]):
    query_filter_carts_by_user: BaseQueryFilterCartsByUserService

    def handle(
        self,
        command: ProfilePageCommand,
    ) -> DTOResponseProfileAPI:
        if not command.is_authenticated:
            raise AuthenticationError("User is not authenticated.")

        # value objects
        username = vo.UserName(command.username)

        packet: List[CartEntity] = self.query_filter_carts_by_user.get_carts_user(
            username=username,
        )
        form = ProfileDataSchema(
            first_name=command.user.first_name,
            last_name=command.user.last_name,
            username=command.user.username,
            email=command.user.email,
            phone=command.user.phone,
            image=command.user.image,
        )

        return DTOResponseProfileAPI(
            packet=packet,
            form=form,
        )
