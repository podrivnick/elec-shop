import unittest
from unittest.mock import MagicMock

from core.api.v1.users.dto.responses import DTOResponseLogoutPageAPI
from core.apps.common.exceptions.main import (
    AuthenticationError,
    LogoutUserError,
)
from core.apps.users.use_cases.logout import (
    LogoutCommand,
    LogoutCommandHandler,
)


class TestLogoutCommandHandler(unittest.TestCase):
    def setUp(self):
        self.command_logout_user_service = MagicMock()
        self.handler = LogoutCommandHandler(
            command_logout_user_service=self.command_logout_user_service,
        )

    def test_handle_user_not_authenticated(self):
        command = LogoutCommand(
            username="test_user",
            is_authenticated=False,
            request=MagicMock(),
        )

        with self.assertRaises(AuthenticationError) as context:
            self.handler.handle(command)

        self.assertEqual(str(context.exception), "User is not authenticated.")

    def test_handle_logout_failure(self):
        command = LogoutCommand(
            username="test_user",
            is_authenticated=True,
            request=MagicMock(),
        )
        self.command_logout_user_service.logout_user.side_effect = Exception(
            "Logout failed",
        )

        with self.assertRaises(LogoutUserError) as context:
            self.handler.handle(command)

        self.assertEqual(str(context.exception), "User test_user not logouted")

    def test_handle_successful_logout(self):
        command = LogoutCommand(
            username="test_user",
            is_authenticated=True,
            request=MagicMock(),
        )

        response = self.handler.handle(command)

        self.command_logout_user_service.logout_user.assert_called_once_with(
            request=command.request,
        )
        self.assertEqual(
            response.username,
            DTOResponseLogoutPageAPI(username="test_user").username,
        )
