from django.test import TestCase

from core.api.v1.main.dto.responses import DTOResponseFavoriteAPI
from core.apps.main.services.favorites.favorites import (
    ORMFavoriteProductsIdsFilterService,
)
from core.apps.main.services.universal import (
    ORMAllProductsService,
    ORMFavoriteProductsIdsService,
)
from core.apps.main.use_cases.favorite import (
    FavoritePageCommand,
    FavoritePageCommandHandler,
)


class TestFavoritePageCommandHandlerIntegration(TestCase):
    def setUp(self):
        self.favorite_products_service_ids = ORMFavoriteProductsIdsService()
        self.get_all_products_service = ORMAllProductsService()
        self.products_service = ORMFavoriteProductsIdsFilterService()

        self.command_handler = FavoritePageCommandHandler(
            favorite_products_service_ids=self.favorite_products_service_ids,
            get_all_products_service=self.get_all_products_service,
            products_service=self.products_service,
        )

    def test_handle_unauthenticated_user(self):
        """Проверяем, что неавторизованный пользователь получает пустой список
        продуктов."""
        command = FavoritePageCommand(is_authenticated=False)

        response = self.command_handler.handle(command)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, DTOResponseFavoriteAPI)
        self.assertEqual(response.products, [])

    def test_handle_user_with_no_favorites(self):
        """Проверяем, что авторизованный пользователь без избранного получает
        пустой список продуктов."""
        command = FavoritePageCommand(is_authenticated=True, username="test_user")

        self.favorite_products_service_ids.get_ids_products_in_favorite = (
            lambda username: []
        )

        response = self.command_handler.handle(command)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, DTOResponseFavoriteAPI)
        self.assertEqual(response.products, [])

    def test_handle_user_with_favorites(self):
        """Проверяем, что авторизованный пользователь с избранными продуктами
        получает отфильтрованный список."""
        command = FavoritePageCommand(is_authenticated=True, username="test_user")

        favorite_products_ids = [1, 2, 3]
        self.favorite_products_service_ids.get_ids_products_in_favorite = (
            lambda username: favorite_products_ids
        )

        all_products = [
            {"id": 1, "title": "Product 1"},
            {"id": 2, "title": "Product 2"},
            {"id": 4, "title": "Product 4"},
        ]
        self.get_all_products_service.get_all_products = lambda: all_products

        filtered_products = [
            {"id": 1, "title": "Product 1"},
            {"id": 2, "title": "Product 2"},
        ]
        self.products_service.get_filtered_products_by_favorite_ids = (
            lambda products, ids_products_in_favorite: filtered_products
        )

        response = self.command_handler.handle(command)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, DTOResponseFavoriteAPI)
        self.assertEqual(response.products, filtered_products)
