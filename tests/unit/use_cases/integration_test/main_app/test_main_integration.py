from django.test import TestCase

from core.api.v1.main.schemas import FiltersProductsSchema
from core.apps.main.services.main.main import (
    ORMCategoriesService,
    ORMProductsService,
)
from core.apps.main.services.universal import (
    ORMAllProductsService,
    ORMFavoriteProductsIdsService,
)
from core.apps.main.use_cases.main import (
    MainPageCommand,
    MainPageCommandHandler,
)


class TestMainPageCommandHandlerIntegration(TestCase):
    def setUp(self):
        self.favorite_products_service_ids = ORMFavoriteProductsIdsService()
        self.get_all_products_service = ORMAllProductsService()
        self.categories_service = ORMCategoriesService()
        self.products_service = ORMProductsService()

        self.command_handler = MainPageCommandHandler(
            favorite_products_service_ids=self.favorite_products_service_ids,
            get_all_products_service=self.get_all_products_service,
            categories_service=self.categories_service,
            products_service=self.products_service,
        )

        self.command = MainPageCommand(
            is_authenticated=True,
            username="test_user",
            filters=FiltersProductsSchema(search="Test"),
            page_number=1,
            category_slug="all",
        )

    def test_handle_main_page_command(self):
        response = self.command_handler.handle(self.command)

        self.assertIsNotNone(response)
        self.assertIsNotNone(response.favorites)
        self.assertIsNotNone(response.categories)
        self.assertIsNotNone(response.products)
        self.assertTrue(response.is_search_failed)
