import unittest
from unittest.mock import MagicMock

from core.apps.carts_products.use_cases.finalize import (
    FinalizePageCommand,
    FinalizePageCommandHandler,
)
from core.apps.common.exceptions.main import AuthenticationError
from core.apps.orders.schemas.main import OrderSchema


class TestFinalizePageCommandHandler(unittest.TestCase):
    def setUp(self):
        self.query_get_user_model_by_username = MagicMock()
        self.query_get_carts_service = MagicMock()

        self.handler = FinalizePageCommandHandler(
            query_get_user_model_by_username=self.query_get_user_model_by_username,
            query_get_carts_service=self.query_get_carts_service,
        )

    def test_handle_with_authenticated_user(self):
        command = FinalizePageCommand(
            is_authenticated=True,
            username="testuser",
        )

        user = MagicMock()
        cart_entity = MagicMock(products_price=100)
        carts = [cart_entity]

        self.query_get_user_model_by_username.get_usermodel_by_username.return_value = (
            user
        )
        self.query_get_carts_service.get_all_carts_by_user.return_value = [carts]

        response = self.handler.handle(command)

        self.query_get_user_model_by_username.get_usermodel_by_username.assert_called_once_with(
            username="testuser",
        )
        self.query_get_carts_service.get_all_carts_by_user.assert_called_once_with(
            filters={"user": user},
        )

        self.assertEqual(response.carts, carts)
        self.assertEqual(response.total_price, 100)
        self.assertIsInstance(response.form, OrderSchema)

    def test_handle_with_unauthenticated_user(self):
        command = FinalizePageCommand(
            is_authenticated=False,
            username=None,
        )

        with self.assertRaises(AuthenticationError):
            self.handler.handle(command)

    def test_total_price_carts(self):
        cart1 = MagicMock(products_price=50)
        cart2 = MagicMock(products_price=150)
        carts = [cart1, cart2]

        total_price = self.handler.total_price_carts(carts)
        self.assertEqual(total_price, 200)

    def test_formating_data_of_user_to_form(self):
        user = MagicMock(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="123456789",
        )

        form = self.handler.formating_data_of_user_to_form(user)

        self.assertEqual(form.first_name, "John")
        self.assertEqual(form.last_name, "Doe")
        self.assertEqual(form.email, "john.doe@example.com")
        self.assertEqual(form.phone, "123456789")
