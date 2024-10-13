import unittest
from unittest.mock import MagicMock

from core.api.v1.users.dto.responses import DTOResponseRegisterAPI
from core.apps.common.exceptions.main import AuthenticationError
from core.apps.users import value_objects as vo
from core.apps.users.entities.user import User as UserEntity
from core.apps.users.exceptions.main import (
    UserNotAuthenticatedError,
    UserNotVerifiedError,
)
from core.apps.users.use_cases.registration import (
    RegisterCommand,
    RegisterCommandHandler,
)


class TestRegisterCommandHandler(unittest.TestCase):
    def setUp(self):
        self.query_verificate_user_is_not_exist = MagicMock()
        self.command_create_user_by_enter_data = MagicMock()
        self.command_authenticate_user_service = MagicMock()
        self.command_add_packet_to_user_by_session_key = MagicMock()

        self.handler = RegisterCommandHandler(
            query_verificate_user_is_not_exist=self.query_verificate_user_is_not_exist,
            command_create_user_by_enter_data=self.command_create_user_by_enter_data,
            command_authenticate_user_service=self.command_authenticate_user_service,
            command_add_packet_to_user_by_session_key=self.command_add_packet_to_user_by_session_key,
        )

    def test_handle_user_authenticated(self):
        command = RegisterCommand(
            first_name="John",
            last_name="Doe",
            username="johndoe",
            email="john@example.com",
            password1="228229122345ARZhjhj",
            password2="228229122345ARZhjhj",
            session_key="some_session_key",
            is_authenticated=True,
            request=None,
        )

        with self.assertRaises(AuthenticationError) as context:
            self.handler.handle(command)

        self.assertEqual(str(context.exception), "User is authenticated.")

    def test_handle_user_already_exists(self):
        command = RegisterCommand(
            first_name="John",
            last_name="Doe",
            username="johndoe",
            email="john@example.com",
            password1="228229122345ARZhjhj",
            password2="228229122345ARZhjhj",
            session_key="some_session_key",
            is_authenticated=False,
            request=None,
        )

        user_entity = MagicMock()
        self.query_verificate_user_is_not_exist.verificate_user.return_value = (
            user_entity
        )

        with self.assertRaises(UserNotVerifiedError) as context:
            self.handler.handle(command)

        self.assertEqual(str(context.exception), "User Verified")

    def test_handle_successful_registration(self):
        command = RegisterCommand(
            first_name="John",
            last_name="Doe",
            username="johndoe",
            email="john@example.com",
            password1="228229122345ARZhjhj",
            password2="228229122345ARZhjhj",
            session_key="some_session_key",
            is_authenticated=False,
            request=MagicMock(),
        )

        # value objects
        entity_user = UserEntity.create_user(
            username=vo.UserName(command.username),
            password=vo.Password(command.password1),
            first_name=vo.FirstName(command.first_name),
            last_name=vo.LastName(command.last_name),
            email=vo.Email(command.email),
            password2=vo.Password(command.password2),
        )

        self.query_verificate_user_is_not_exist.verificate_user.return_value = None
        self.command_create_user_by_enter_data.create_user.return_value = entity_user

        response = self.handler.handle(command)

        self.query_verificate_user_is_not_exist.verificate_user.assert_called_once()
        self.command_create_user_by_enter_data.create_user.assert_called_once_with(
            user=entity_user,
        )
        self.command_authenticate_user_service.login.assert_called_once_with(
            user=entity_user,
            request=command.request,
        )
        self.command_add_packet_to_user_by_session_key.add_packet_to_user_by_session_key.assert_called_once_with(
            user=entity_user,
            session_key=command.session_key,
        )

        self.assertIsInstance(response, DTOResponseRegisterAPI)
        self.assertEqual(response.username, command.username)

    def test_handle_authentication_failure(self):
        command = RegisterCommand(
            first_name="John",
            last_name="Doe",
            username="johndoe",
            email="john@example.com",
            password1="228229122345ARZhjhj",
            password2="228229122345ARZhjhj",
            session_key="some_session_key",
            is_authenticated=False,
            request=MagicMock(),
        )

        entity_user = MagicMock()
        self.query_verificate_user_is_not_exist.verificate_user.return_value = None
        self.command_create_user_by_enter_data.create_user.return_value = entity_user

        self.command_authenticate_user_service.login.side_effect = Exception(
            "Authentication failed",
        )

        with self.assertRaises(UserNotAuthenticatedError) as context:
            self.handler.handle(command)

        self.assertEqual(
            str(context.exception),
            f"{command.username} not authenticated",
        )

    def test_handle_error_adding_packet(self):
        command = RegisterCommand(
            first_name="John",
            last_name="Doe",
            username="johndoe",
            email="john@example.com",
            password1="228229122345ARZhjhj",
            password2="228229122345ARZhjhj",
            session_key="some_session_key",
            is_authenticated=False,
            request=MagicMock(),
        )

        entity_user = MagicMock()
        self.query_verificate_user_is_not_exist.verificate_user.return_value = None
        self.command_create_user_by_enter_data.create_user.return_value = entity_user

        # Mock packet service failure
        self.command_add_packet_to_user_by_session_key.add_packet_to_user_by_session_key.side_effect = Exception(
            "Packet error",
        )

        with self.assertRaises(ValueError) as context:
            self.handler.handle(command)

        self.assertEqual(str(context.exception), "Some Error In Server")
