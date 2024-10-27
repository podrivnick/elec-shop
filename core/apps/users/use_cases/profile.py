from dataclasses import (
    dataclass,
    field,
)
from typing import (
    List,
    Optional,
)

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.functional import SimpleLazyObject
from django.utils.safestring import SafeString

from core.api.v1.users.dto.responses import DTOResponseProfileAPI
from core.apps.common.exceptions.main import AuthenticationError
from core.apps.common.services.base import BaseQueryGetUserModelService
from core.apps.packet.entities.cart import CartEntity
from core.apps.users import value_objects as vo
from core.apps.users.entities.user import User as UserEntity
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
    updated_information: Optional[ProfileDataSchema] | None = field(default=None)


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
        username = vo.UserName(command.user.username)
        first_name = vo.FirstName(command.user.first_name)
        last_name = vo.LastName(command.user.last_name)
        age = vo.AgeUser(command.user.age)
        image = vo.ImageUser(command.user.image)
        phone = vo.PhoneNumber(command.user.phone)
        email = vo.Email(command.user.email)

        if command.updated_information:
            # value objects
            updated_first_name = vo.FirstName(command.updated_information.first_name)
            updated_last_name = vo.LastName(command.updated_information.last_name)
            updated_age = vo.AgeUser(command.updated_information.age)
            updated_phone = vo.PhoneNumber(command.updated_information.phone)
            updated_email = vo.Email(command.updated_information.email)

            # entity
            user_entity = UserEntity.create_user(
                first_name=updated_first_name,
                last_name=updated_last_name,
                age=updated_age,
                phone=updated_phone,
                email=updated_email,
            )
            self._update_profile_info(username, user_entity)

        packet: List[CartEntity] = self.query_filter_carts_by_user.get_carts_user(
            username=username,
        )

        form = ProfileDataSchema(
            first_name=first_name.to_raw(),
            last_name=last_name.to_raw(),
            username=username.to_raw(),
            email=email.to_raw(),
            phone=phone.to_raw(),
            image=image.to_raw(),
            age=age.to_raw(),
        )

        return DTOResponseProfileAPI(
            packet=packet,
            form=form,
            referer=command.referer,
        )

    def _update_profile_info(
        self,
        username: vo.UserName,
        updated_information: UserEntity,
    ):
        user_model = self.query_get_user_model.get_usermodel_by_username(
            username=username.to_raw(),
        )
        if not user_model:
            raise ValueError("Some Error In Server")

        updated_data = (
            self.query_validate_new_information.validate_new_information_user(
                user=user_model,
                new_data=updated_information,
            )
        )

        if updated_data:
            self.command_set_updated_information_of_user.set_information_user(
                user=user_model,
                updated_information=updated_data,
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
            # value objects
            updated_username = vo.UserName(command.updated_data.username)
            updated_image = vo.ImageUser(command.updated_data.image)

            # entity
            user_entity = UserEntity.create_user(
                username=updated_username,
                image=updated_image,
            )

            self._update_profile_info(
                username=username,
                updated_data=user_entity,
            )

    def _update_profile_info(self, username: vo.UserName, updated_data: UserEntity):
        user_model = self.query_get_user_model.get_usermodel_by_username(
            username=username.to_raw(),
        )
        if not user_model:
            raise ValueError("Some Error In Server")

        updated_information = (
            self.query_validate_new_information.validate_new_information_user(
                user=user_model,
                new_data=updated_data,
            )
        )
        if updated_information:
            self.command_set_updated_information_of_user.set_information_user(
                user=user_model,
                updated_information=updated_information,
            )


@dataclass(frozen=True)
class ChangeTabCommand(BaseCommands):
    is_authenticated: bool = field(default=False)
    is_packet: Optional[str] | None = field(default=None)
    request: HttpRequest | None = field(default=None)


@dataclass(frozen=True)
class ChangeTabCommandHandler(CommandHandler[ChangeTabCommand, str]):
    def handle(
        self,
        command: ChangeTabCommand,
    ) -> SafeString:
        if not command.is_authenticated:
            raise AuthenticationError("User is not authenticated.")
        if command.is_packet == "order":
            carts_items_user = render_to_string(
                "users/packet_profile/orders_profile.html",
                {"is_packet": False},
                request=command.request,
            )
        else:
            carts_items_user = render_to_string(
                "users/packet_profile/packet_profile.html",
                {"is_packet": True},
                request=command.request,
            )
        return carts_items_user
