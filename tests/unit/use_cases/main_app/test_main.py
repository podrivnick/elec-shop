from unittest.mock import Mock

from core.api.v1.main.schemas import FiltersProductsSchema
from core.apps.main.use_cases.main import (
    MainPageCommand,
    MainPageCommandHandler,
)


def test_use_case_calls_correct_service():
    # Mocks
    favorite_products_service_ids = Mock()
    get_all_products_service = Mock()
    categories_service = Mock()
    products_service = Mock()

    # Configure Mock services
    get_all_products_service.get_all_products.return_value = ["product1", "product2"]
    favorite_products_service_ids.get_ids_products_in_favorite.return_value = [1, 2]
    categories_service.get_all_products_categories.return_value = [
        "category1",
        "category2",
    ]
    products_service.get_filtered_products.return_value = (
        False,
        ["product1_filtered", "product2_filtered"],
    )
    products_service.paginate_products.return_value = [
        "paginated_product1",
        "paginated_product2",
    ]

    command = MainPageCommand(
        is_authenticated=True,
        username="user123",
        filters=FiltersProductsSchema(
            available="on_available",
            discount="on_discount",
            sorting="-price",
        ),
        page_number=1,
        category_slug="all",
    )

    use_case = MainPageCommandHandler(
        favorite_products_service_ids=favorite_products_service_ids,
        get_all_products_service=get_all_products_service,
        categories_service=categories_service,
        products_service=products_service,
    )

    result = use_case.handle(command)

    get_all_products_service.get_all_products.assert_called_once()
    favorite_products_service_ids.get_ids_products_in_favorite.assert_called_once_with(
        "user123",
    )
    categories_service.get_all_products_categories.assert_called_once()
    products_service.get_filtered_products.assert_called_once_with(
        products=["product1", "product2"],
        filters=command.filters,
        category_slug=command.category_slug,
    )
    products_service.paginate_products.assert_called_once_with(
        page_number=command.page_number,
        products=["product1_filtered", "product2_filtered"],
    )

    assert result.favorites == [1, 2]
    assert result.categories == ["category1", "category2"]
    assert result.is_search_failed is False
    assert result.products == ["paginated_product1", "paginated_product2"]
