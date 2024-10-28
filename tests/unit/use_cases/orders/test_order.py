import unittest
from unittest.mock import Mock

from core.api.v1.orders.dto.responses import DTOResponseOrderAPI
from core.apps.common.exceptions.main import AuthenticationError
from core.apps.common.services.base import BaseQueryGetUserModelService
from core.apps.orders.exceptions.order import OrderNotCreatedError
from core.apps.orders.repositories.base import BaseCommandOrderRepository
from core.apps.orders.services.base import (
    BaseCommandOrderService,
    BaseQueryValidationOrderService,
)
from core.apps.orders.use_cases.order import (
    OrderCommand,
    OrderCommandHandler,
)
from core.apps.packet.services.base import BaseQueryGetCartService


class OrderCommandHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.user_service = Mock(BaseQueryGetUserModelService)
        self.validation_service = Mock(BaseQueryValidationOrderService)
        self.basic_order_service = Mock(BaseCommandOrderService)
        self.cart_service = Mock(BaseQueryGetCartService)
        self.order_repository = Mock(BaseCommandOrderRepository)

        self.handler = OrderCommandHandler(
            query_get_user_model_by_username=self.user_service,
            query_validation_order_data_service=self.validation_service,
            command_create_basic_order=self.basic_order_service,
            query_filter_packet_service=self.cart_service,
            command_order_repository=self.order_repository,
        )

    def test_handle_authenticated_user_success(self):
        command = OrderCommand(
            is_authenticated=True,
            username="test_user",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            delivery_address="123 Test St",
            required_delivery="standard",
            payment_on_get="yes",
            total_price="100.0",
        )

        self.user_service.get_usermodel_by_username.return_value = Mock()
        self.validation_service.validate_order_data.return_value = Mock()
        self.basic_order_service.create_basic_order.return_value = Mock()
        self.cart_service.get_carts_by_user_quantity.return_value = [Mock(), Mock()]

        response = self.handler.handle(command)

        self.assertIsInstance(response, DTOResponseOrderAPI)
        self.assertEqual(response.username, command.username)
        self.user_service.get_usermodel_by_username.assert_called_once_with(
            username="test_user",
        )
        self.validation_service.validate_order_data.assert_called_once()
        self.basic_order_service.create_basic_order.assert_called_once()
        self.cart_service.get_carts_by_user_quantity.assert_called_once()

    def test_handle_not_authenticated_user_raises_error(self):
        command = OrderCommand(
            is_authenticated=False,
            username="test_user",
        )

        with self.assertRaises(AuthenticationError):
            self.handler.handle(command)

    def test_handle_order_creation_fails_and_order_is_deleted(self):
        command = OrderCommand(
            is_authenticated=True,
            username="test_user",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            delivery_address="123 Test St",
            required_delivery="standard",
            payment_on_get="yes",
            total_price="100.0",
        )

        self.user_service.get_usermodel_by_username.return_value = Mock()
        self.validation_service.validate_order_data.return_value = Mock()
        self.basic_order_service.create_basic_order.return_value = Mock()
        self.cart_service.get_carts_by_user_quantity.return_value = [Mock(), Mock()]

        self.basic_order_service.create_orders_items.side_effect = Exception(
            "Order items creation failed",
        )

        with self.assertRaises(OrderNotCreatedError):
            self.handler.handle(command)

        self.order_repository.delete_basic_order.assert_called_once()
