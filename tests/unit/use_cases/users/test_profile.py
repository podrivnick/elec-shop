import unittest
from unittest.mock import MagicMock

from core.apps.common.exceptions.main import AuthenticationError
from core.apps.users.schemas.user_profile import ProfileDataSchema
from core.apps.users.use_cases.profile import (
    ProfileCommand,
    ProfileCommandHandler,
)


class TestProfileCommandHandler(unittest.TestCase):
    def setUp(self):
        self.query_validate_new_information = MagicMock()
        self.query_get_user_model = MagicMock()
        self.command_set_updated_information_of_user = MagicMock()

        self.handler = ProfileCommandHandler(
            query_validate_new_information=self.query_validate_new_information,
            query_get_user_model=self.query_get_user_model,
            command_set_updated_information_of_user=self.command_set_updated_information_of_user,
        )

    def test_handle_user_not_authenticated(self):
        command = ProfileCommand(
            user=MagicMock(),
            username="test_user",
            is_authenticated=False,
            updated_data=None,
        )

        with self.assertRaises(AuthenticationError) as context:
            self.handler.handle(command)

        self.assertEqual(str(context.exception), "User is not authenticated.")

    def test_handle_no_updated_data(self):
        command = ProfileCommand(
            user=MagicMock(),
            username="test_user",
            is_authenticated=True,
            updated_data=None,
        )

        self.handler.handle(command)

        # Ensure no updates are attempted when no updated_data is provided
        self.query_get_user_model.get_usermodel_by_username.assert_not_called()
        self.query_validate_new_information.validate_new_information_user.assert_not_called()
        self.command_set_updated_information_of_user.set_information_user.assert_not_called()

    def test_handle_successful_update(self):
        updated_data_schema = ProfileDataSchema(
            username="new_username",
            image="new_image",
        )
        command = ProfileCommand(
            user=MagicMock(),
            username="test_user",
            is_authenticated=True,
            updated_data=updated_data_schema,
        )

        self.query_get_user_model.get_usermodel_by_username.return_value = MagicMock()
        self.query_validate_new_information.validate_new_information_user.return_value = {
            "username": "new_username",
            "image": "new_image",
        }

        self.handler.handle(command)

        self.query_get_user_model.get_usermodel_by_username.assert_called_once_with(
            username="test_user",
        )
        self.query_validate_new_information.validate_new_information_user.assert_called_once()
        self.command_set_updated_information_of_user.set_information_user.assert_called_once()

    def test_handle_user_not_found(self):
        updated_data_schema = ProfileDataSchema(
            username="new_username",
            image="new_image",
        )
        command = ProfileCommand(
            user=MagicMock(),
            username="test_user",
            is_authenticated=True,
            updated_data=updated_data_schema,
        )

        self.query_get_user_model.get_usermodel_by_username.return_value = None

        with self.assertRaises(ValueError) as context:
            self.handler.handle(command)

        self.assertEqual(str(context.exception), "Some Error In Server")
