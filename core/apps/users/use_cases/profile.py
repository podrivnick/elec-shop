from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Dict,
    List,
    Optional,
)

from django.utils.functional import SimpleLazyObject

from core.api.v1.users.dto.responses import DTOResponseProfileAPI
from core.apps.common.exceptions.main import AuthenticationError
from core.apps.common.services.base import BaseQueryGetUserModelService
from core.apps.packet.entities.cart import CartEntity
from core.apps.users import value_objects as vo
from core.apps.users.schemas.user_profile import ProfileDataSchema
from core.apps.users.services.profile.base import (
    BaseCommandSetUpdatedInformationOfUserService,
    BaseQueryFilterCartsByUserService,
    BaseQueryValidateNewDataService,
)
from core.infrastructure.mediator.base import BaseCommands
from core.infrastructure.mediator.handlers.commands import CommandHandler


@dataclass(frozen=True)
class ProfilePageCommand(BaseCommands):
    user: SimpleLazyObject
    is_authenticated: bool = field(default=False)
    referer: Optional[str] | None = field(default=None)
    username: Optional[str] | None = field(default=None)
    updated_information: Optional[Dict] | None = field(default=None)


@dataclass(frozen=True)
class ProfilePageCommandHandler(CommandHandler[ProfilePageCommand, str]):
    query_filter_carts_by_user: BaseQueryFilterCartsByUserService
    query_validate_new_information: BaseQueryValidateNewDataService
    query_get_user_model: BaseQueryGetUserModelService
    command_set_updated_information_of_user: (
        BaseCommandSetUpdatedInformationOfUserService
    )

    def handle(
        self,
        command: ProfilePageCommand,
    ) -> DTOResponseProfileAPI:
        if not command.is_authenticated:
            raise AuthenticationError("User is not authenticated.")

        # value objects
        username = vo.UserName(command.username)

        if command.updated_information:
            user_model = self.query_get_user_model.get_usermodel_by_username(
                username=username.to_raw(),
            )
            if not user_model:
                raise ValueError("Some Error In Server")

            updated_data = (
                self.query_validate_new_information.validate_new_information_user(
                    user=user_model,
                    new_data=command.updated_information,
                )
            )
            if updated_data:
                self.command_set_updated_information_of_user.set_information_user(
                    user=user_model,
                    updated_information=updated_data,
                )

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
            age=command.user.age,
        )

        return DTOResponseProfileAPI(
            packet=packet,
            form=form,
            referer=command.referer,
        )


@dataclass(frozen=True)
class ProfileCommand(BaseCommands):
    user: SimpleLazyObject
    username: Optional[str] | None = field(default=None)
    is_authenticated: bool = field(default=False)
    updated_data: Optional[ProfileDataSchema] | None = field(default=None)


@dataclass(frozen=True)
class ProfileCommandHandler(CommandHandler[ProfileCommand, str]):
    query_validate_new_information: BaseQueryValidateNewDataService
    query_get_user_model: BaseQueryGetUserModelService
    command_set_updated_information_of_user: (
        BaseCommandSetUpdatedInformationOfUserService
    )

    def handle(
        self,
        command: ProfileCommand,
    ) -> None:
        if not command.is_authenticated:
            raise AuthenticationError("User is not authenticated.")

        # value objects
        username = vo.UserName(command.username)

        if command.updated_data:
            user_model = self.query_get_user_model.get_usermodel_by_username(
                username=username.to_raw(),
            )
            if not user_model:
                raise ValueError("Some Error In Server")

            updated_information = (
                self.query_validate_new_information.validate_new_information_user(
                    user=user_model,
                    new_data=command.updated_data,
                )
            )
            if updated_information:
                self.command_set_updated_information_of_user.set_information_user(
                    user=user_model,
                    updated_information=updated_information,
                )
