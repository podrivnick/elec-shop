from datetime import datetime
from unittest.mock import Mock

from core.apps.main.entities.product import ProductEntity
from core.apps.main.use_cases.favorite import (
    FavoritePageCommand,
    FavoritePageCommandHandler,
)


def test_use_case_favorite_calls_correct_service():
    # Mocks
    favorite_products_service_ids = Mock()
    get_all_products_service = Mock()
    products_service = Mock()

    product_1, product_2 = (
        ProductEntity(
            id_product="1",
            name="some",
            description="some descriptions",
            slug="some",
            image="/some/some",
            discount=23,
            price=1000,
            count_product=222,
            category="all",
            created_at=datetime(2024, 10, 10, 14, 30, 45),
            updated_at=datetime(2024, 10, 10, 14, 30, 45),
            headline="some",
            bodyline="some",
        ),
        ProductEntity(
            id_product="2",
            name="some",
            description="some descriptions",
            slug="some",
            image="/some/some",
            discount=0,
            price=2000,
            count_product=222,
            category="all",
            created_at=datetime(2024, 10, 10, 14, 30, 45),
            updated_at=datetime(2024, 10, 10, 14, 30, 45),
            headline="some",
            bodyline="some",
        ),
    )

    # Configure Mock services
    get_all_products_service.get_all_products.return_value = ["product1", "product2"]
    favorite_products_service_ids.get_ids_products_in_favorite.return_value = [1, 2]
    products_service.get_filtered_products_by_favorite_ids.return_value = [
        product_1,
        product_2,
    ]

    command = FavoritePageCommand(
        is_authenticated=True,
        username="user123",
    )

    use_case = FavoritePageCommandHandler(
        favorite_products_service_ids=favorite_products_service_ids,
        get_all_products_service=get_all_products_service,
        products_service=products_service,
    )

    result = use_case.handle(command)

    get_all_products_service.get_all_products.assert_called_once()
    favorite_products_service_ids.get_ids_products_in_favorite.assert_called_once_with(
        "user123",
    )
    products_service.get_filtered_products_by_favorite_ids.assert_called_once_with(
        products=["product1", "product2"],
        ids_products_in_favorite=[1, 2],
    )

    assert result.products == [product_1, product_2]
