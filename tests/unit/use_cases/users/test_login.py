import unittest
from unittest.mock import MagicMock

from core.api.v1.users.dto.responses import DTOResponseAuthenticateAPI
from core.apps.common.exceptions.main import AuthenticationError
from core.apps.users.exceptions.main import (
    UserNotAuthenticatedError,
    UserNotVerifiedError,
)
from core.apps.users.use_cases.login import (
    AuthenticatePageCommand,
    AuthenticatePageCommandHandler,
)


class TestAuthenticatePageCommandHandler(unittest.TestCase):
    def setUp(self):
        self.command_verificate_password_service = MagicMock()
        self.command_authenticate_user_service = MagicMock()
        self.command_add_packet_to_user_by_session_key = MagicMock()

        self.handler = AuthenticatePageCommandHandler(
            command_verificate_password_service=self.command_verificate_password_service,
            command_authenticate_user_service=self.command_authenticate_user_service,
            command_add_packet_to_user_by_session_key=self.command_add_packet_to_user_by_session_key,
        )

    def test_handle_user_authenticated(self):
        command = AuthenticatePageCommand(
            username="test_user",
            password="228229098ASASplpl",
            is_authenticated=True,
            request=MagicMock(),
            session_key="test_session_key",
        )

        with self.assertRaises(AuthenticationError):
            self.handler.handle(command)

    def test_handle_user_not_verified(self):
        command = AuthenticatePageCommand(
            username="test_user",
            password="228229098ASASplpl",
            is_authenticated=False,
            request=MagicMock(),
            session_key="test_session_key",
        )
        self.command_verificate_password_service.verificate_password.return_value = None

        with self.assertRaises(UserNotVerifiedError) as context:
            self.handler.handle(command)

        self.assertEqual(str(context.exception), "User 'test_user' not verified.")

    def test_handle_user_not_authenticated(self):
        command = AuthenticatePageCommand(
            username="test_user",
            password="228229098ASASplpl",
            is_authenticated=False,
            request=MagicMock(),
            session_key="test_session_key",
        )
        entity_user = MagicMock()
        entity_user.username.to_raw.return_value = "test_user"
        self.command_verificate_password_service.verificate_password.return_value = (
            entity_user
        )
        self.command_authenticate_user_service.login.side_effect = Exception(
            "Login failed",
        )

        with self.assertRaises(UserNotAuthenticatedError) as context:
            self.handler.handle(command)

        self.assertEqual(str(context.exception), "test_user not authenticated")

    def test_handle_success(self):
        command = AuthenticatePageCommand(
            username="test_user",
            password="228229098ASASplpl",
            is_authenticated=False,
            request=MagicMock(),
            session_key="test_session_key",
        )
        entity_user = MagicMock()
        entity_user.username.to_raw.return_value = "test_user"
        self.command_verificate_password_service.verificate_password.return_value = (
            entity_user
        )
        self.command_authenticate_user_service.login.return_value = None

        response = self.handler.handle(command)

        self.command_add_packet_to_user_by_session_key.add_packet_to_user_by_session_key.assert_called_once_with(
            user=entity_user,
            session_key="test_session_key",
        )
        self.assertEqual(
            response.username,
            DTOResponseAuthenticateAPI(username="test_user").username,
        )
