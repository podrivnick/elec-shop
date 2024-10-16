from unittest.mock import (
    MagicMock,
    patch,
)

from django.contrib.sessions.backends.cache import SessionStore
from django.http import HttpRequest

import pytest

from core.api.v1.packet.dto.responses import (
    DTOResponseAddPacketAPI,
    DTOResponseUpdatePacketAPI,
)
from core.apps.packet.exceptions.main import DatabaseCartError
from core.apps.packet.use_cases.packet import (
    AddPacketCommand,
    AddPacketCommandHandler,
    ChangePacketCommand,
    ChangePacketCommandHandler,
    DeletePacketCommand,
    DeletePacketCommandHandler,
)


@pytest.fixture
def http_request():
    req = HttpRequest()
    req.session = SessionStore()  # Инициализируем сессии
    req.session["session_key"] = (
        "test_session_key"  # Добавьте любые ключи сессии, которые вам нужны
    )

    return req


@pytest.fixture
def command(http_request):
    return ChangePacketCommand(
        is_plus=1,
        cart_id=1,
        is_profile="false",
        is_authenticated=True,
        username="johndoe",
        session_key="test_session_key",
        request=http_request,
    )


@pytest.fixture
def handler(command):
    command_change_quantity_cart_from_packet = MagicMock()
    query_get_user_model = MagicMock()
    query_get_cart = MagicMock()

    return ChangePacketCommandHandler(
        command_change_quantity_cart_from_packet=command_change_quantity_cart_from_packet,
        query_get_user_model=query_get_user_model,
        query_get_cart=query_get_cart,
    )


def test_handle_authenticated_user(handler, command):
    mock_user = MagicMock()
    handler.query_get_user_model.get_usermodel_by_username.return_value = mock_user
    mock_cart = MagicMock(quantity=1)
    handler.query_get_cart.get_cart_by_id.return_value = mock_cart
    handler.command_change_quantity_cart_from_packet.process_change_quantity_products_in_packet.return_value = None
    handler.query_get_cart.get_all_carts_by_user.return_value = ([], 0)

    with patch.object(ChangePacketCommandHandler, "_render_template") as mock_render:
        mock_render.return_value = "mocked_rendered_string"

        result = handler.handle(command)

        handler.query_get_user_model.get_usermodel_by_username.assert_called_once_with(
            username="johndoe",
        )
        handler.query_get_cart.get_cart_by_id.assert_called_once_with(cart_id=1)
        handler.command_change_quantity_cart_from_packet.process_change_quantity_products_in_packet.assert_called_once_with(
            cart_id=1,
            is_plus=1,
            cart=mock_cart,
        )
        handler.query_get_cart.get_all_carts_by_user.assert_called_once_with(
            filters={"user": mock_user},
        )

        assert isinstance(result, DTOResponseUpdatePacketAPI)
        assert result.carts_items_user is not None
        assert result.new_quantity == 0


def test_handle_cart_not_found(handler, command):
    handler.query_get_cart.get_cart_by_id.return_value = (
        None  # Мокируем отсутствие корзины
    )

    with pytest.raises(DatabaseCartError, match="Not Found Cart"):
        handler.handle(command)

    handler.query_get_cart.get_cart_by_id.assert_called_once_with(cart_id=1)


def test_handle_not_authenticated_user(handler, command):
    not_authenticated_command = ChangePacketCommand(
        is_plus=command.is_plus,
        cart_id=command.cart_id,
        is_profile=command.is_profile,
        is_authenticated=False,
        username=command.username,
        session_key=command.session_key,
        request=command.request,
    )

    handler.query_get_cart.get_cart_by_id.return_value = MagicMock(quantity=1)
    handler.query_get_cart.get_all_carts_by_user.return_value = ([], 0)

    with patch.object(ChangePacketCommandHandler, "_render_template") as mock_render:
        mock_render.return_value = "mocked_rendered_string"

        result = handler.handle(not_authenticated_command)

        handler.query_get_cart.get_cart_by_id.assert_called_once_with(cart_id=1)
        handler.query_get_cart.get_all_carts_by_user.assert_called_once_with(
            filters={
                "session_key": command.session_key,
            },  # Проверка, что фильтр был правильным
        )

        assert result.new_quantity == 0


def test_handle_rendering_for_profile(handler, command):
    is_profile_command = ChangePacketCommand(
        is_plus=command.is_plus,
        cart_id=command.cart_id,
        is_profile="true",
        is_authenticated=command.is_authenticated,
        username=command.username,
        session_key=command.session_key,
        request=command.request,
    )
    mock_cart = MagicMock(quantity=1)
    handler.query_get_cart.get_cart_by_id.return_value = mock_cart
    handler.query_get_cart.get_all_carts_by_user.return_value = ([], 0)

    with patch.object(ChangePacketCommandHandler, "_render_template") as mock_render:
        mock_render.return_value = "mocked_rendered_string"

        result = handler.handle(is_profile_command)

        mock_render.assert_called_once_with(
            is_profile="true",
            packet=[],
            request=is_profile_command.request,
        )
        assert result.carts_items_user == "mocked_rendered_string"


@pytest.fixture
def handler_delete():
    return DeletePacketCommandHandler(
        command_delete_cart_from_packet=MagicMock(),
        query_get_user_model=MagicMock(),
        query_get_cart_by_user=MagicMock(),
    )


@pytest.fixture
def command_delete():
    return DeletePacketCommand(
        cart_id=1,
        is_profile="true",
        is_authenticated=True,
        username="johndoe",
        session_key="test_session_key",
        request=HttpRequest(),
    )


def test_handle_authenticated_user_delete(handler_delete, command_delete):
    mock_user = MagicMock(username="johndoe")

    handler_delete.command_delete_cart_from_packet.delete_cart_from_packet.return_value = None
    handler_delete.query_get_user_model.get_usermodel_by_username.return_value = (
        mock_user
    )
    handler_delete.query_get_cart_by_user.get_all_carts_by_user.return_value = ([], 0)

    with patch.object(DeletePacketCommandHandler, "_render_template") as mock_render:
        mock_render.return_value = "mocked_rendered_string"

        result = handler_delete.handle(command_delete)

        handler_delete.command_delete_cart_from_packet.delete_cart_from_packet.assert_called_once_with(
            cart_id=1,
        )

        handler_delete.query_get_user_model.get_usermodel_by_username.assert_called_once_with(
            username="johndoe",
        )

        handler_delete.query_get_cart_by_user.get_all_carts_by_user.assert_called_once_with(
            filters={"user": mock_user},
        )

        mock_render.assert_called_once_with(
            is_profile="true",
            packet=[],
            request=command_delete.request,
        )

        assert isinstance(result, DTOResponseUpdatePacketAPI)
        assert result.carts_items_user == "mocked_rendered_string"
        assert result.new_quantity == 0


def test_handle_not_authenticated_user_delete(handler_delete, command_delete):
    command_delete = command_delete.__class__(
        cart_id=1,
        is_profile="false",
        is_authenticated=False,
        username=None,
        session_key="test_session_key",
        request=command_delete.request,
    )

    handler_delete.command_delete_cart_from_packet.delete_cart_from_packet.return_value = None
    handler_delete.query_get_cart_by_user.get_all_carts_by_user.return_value = ([], 0)

    with patch.object(DeletePacketCommandHandler, "_render_template") as mock_render:
        mock_render.return_value = "mocked_rendered_string"

        result = handler_delete.handle(command_delete)

        handler_delete.command_delete_cart_from_packet.delete_cart_from_packet.assert_called_once_with(
            cart_id=1,
        )

        handler_delete.query_get_cart_by_user.get_all_carts_by_user.assert_called_once_with(
            filters={"session_key": command_delete.session_key},
        )

        mock_render.assert_called_once_with(
            is_profile="false",
            packet=[],
            request=command_delete.request,
        )

        assert isinstance(result, DTOResponseUpdatePacketAPI)
        assert result.carts_items_user == "mocked_rendered_string"
        assert result.new_quantity == 0


def test_handle_packet_not_found_delete(handler_delete, command_delete):
    handler_delete.command_delete_cart_from_packet.delete_cart_from_packet.side_effect = Exception(
        "Packet not found",
    )

    with pytest.raises(Exception):
        handler_delete.handle(command_delete)


# ADD PACKET USE CASE TESTS


@pytest.fixture
def handler_add():
    return AddPacketCommandHandler(
        query_get_user_model=MagicMock(),
        query_get_product_by_id=MagicMock(),
        query_get_cart_by_product_and_user=MagicMock(),
        command_update_or_create_cart=MagicMock(),
    )


def test_handle_authenticated_user_add(handler_add):
    # Настройка тестовых данных
    command = AddPacketCommand(
        is_authenticated=True,
        username="TestUser",
        product_id=1,
        session_key=None,
        request=MagicMock(),  # Мокаем HttpRequest
    )

    # Мокаем методы для теста
    mock_user = MagicMock()
    handler_add.query_get_user_model.get_usermodel_by_username.return_value = mock_user
    mock_product = MagicMock()
    handler_add.query_get_product_by_id.get_product_by_id.return_value = mock_product
    mock_packet = MagicMock()
    handler_add.query_get_cart_by_product_and_user.get_cart_by_product_and_user.return_value = mock_packet
    updated_packet = MagicMock()
    handler_add.command_update_or_create_cart.update_or_create_cart.return_value = (
        updated_packet
    )

    with patch.object(AddPacketCommandHandler, "_render_template") as mock_render:
        mock_render.return_value = "mocked_rendered_string"

        result = handler_add.handle(command)

        handler_add.query_get_user_model.get_usermodel_by_username.assert_called_once_with(
            username="TestUser",
        )
        handler_add.query_get_product_by_id.get_product_by_id.assert_called_once_with(
            id_product=1,
        )
        handler_add.query_get_cart_by_product_and_user.get_cart_by_product_and_user.assert_called_once_with(
            product=mock_product,
            filters={"user": mock_user},
        )
        handler_add.command_update_or_create_cart.update_or_create_cart.assert_called_once_with(
            product=mock_product,
            packet=mock_packet,
            filters={"user": mock_user},
        )
        mock_render.assert_called_once_with(
            packet=updated_packet,
            request=command.request,
        )

        assert isinstance(result, DTOResponseAddPacketAPI)
        assert result.carts_items_user == "mocked_rendered_string"


def test_handle_not_authenticated_user_add(handler_add):
    command = AddPacketCommand(
        is_authenticated=False,
        username=None,
        product_id=1,
        session_key="test_session_key",
        request=MagicMock(),  # Мокаем HttpRequest
    )

    mock_product = MagicMock()
    handler_add.query_get_product_by_id.get_product_by_id.return_value = mock_product
    mock_packet = MagicMock()
    handler_add.query_get_cart_by_product_and_user.get_cart_by_product_and_user.return_value = mock_packet
    updated_packet = MagicMock()
    handler_add.command_update_or_create_cart.update_or_create_cart.return_value = (
        updated_packet
    )

    with patch.object(AddPacketCommandHandler, "_render_template") as mock_render:
        mock_render.return_value = "mocked_rendered_string"

        result = handler_add.handle(command)

        handler_add.query_get_product_by_id.get_product_by_id.assert_called_once_with(
            id_product=1,
        )
        handler_add.query_get_cart_by_product_and_user.get_cart_by_product_and_user.assert_called_once_with(
            product=mock_product,
            filters={"session_key": "test_session_key"},
        )
        handler_add.command_update_or_create_cart.update_or_create_cart.assert_called_once_with(
            product=mock_product,
            packet=mock_packet,
            filters={"session_key": "test_session_key"},
        )
        mock_render.assert_called_once_with(
            packet=updated_packet,
            request=command.request,
        )

        assert isinstance(result, DTOResponseAddPacketAPI)
        assert result.carts_items_user == "mocked_rendered_string"
