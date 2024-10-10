from unittest.mock import Mock

from core.apps.main.use_cases.update_favorite import (
    UpdateFavoritePageCommand,
    UpdateFavoritePageCommandHandler,
)


def test_use_case_update_favorite_calls_correct_service():
    # Mocks
    query_get_user_model_by_username = Mock()
    query_update_favorite_product_service = Mock()
    command_update_favorite_product_service = Mock()

    # Configure Mock services
    query_get_user_model_by_username.get_usermodel_by_username.return_value = "user123"
    query_update_favorite_product_service.check_product_in_favorite_is_exist.return_value = False
    command_update_favorite_product_service.add_product_to_favorite.return_value = None

    command = UpdateFavoritePageCommand(
        product_id=1,
        is_authenticated=True,
        username="user123",
    )

    use_case = UpdateFavoritePageCommandHandler(
        query_get_user_model_by_username=query_get_user_model_by_username,
        query_update_favorite_product_service=query_update_favorite_product_service,
        command_update_favorite_product_service=command_update_favorite_product_service,
    )

    use_case.handle(command)

    query_get_user_model_by_username.get_usermodel_by_username.assert_called_once_with(
        username="user123",
    )
    query_update_favorite_product_service.check_product_in_favorite_is_exist.assert_called_once_with(
        username="user123",
        product_id=1,
    )
    command_update_favorite_product_service.add_product_to_favorite.assert_called_once_with(
        user="user123",
        product_id=1,
    )
