from django.test import TestCase
from django.contrib.auth import get_user_model
from core.apps.main.models.products import Products
from core.apps.main.models.favorites import Favorites
from core.api.v1.main.dto.responses import DTOResponseFavoriteAPI
from core.apps.main.services.favorites.favorites import (
    ORMFavoriteProductsIdsFilterService,
)
from core.apps.main.models.products import CategoriesProduct
from core.apps.main.services.universal import (
    ORMAllProductsService,
    ORMFavoriteProductsIdsService,
)
from core.apps.main.use_cases.favorite import (
    FavoritePageCommand,
    FavoritePageCommandHandler,
)


User = get_user_model()


class TestFavoritePageCommandHandlerIntegration(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="test_user")
        self.categories = CategoriesProduct.objects.create(category="all")

        self.product_1 = Products.objects.create(
            name="Product 1",
            category_id=self.categories.id,
        )
        self.product_2 = Products.objects.create(
            name="Product 2",
            category_id=self.categories.id,
        )

        self.favorite_products_service_ids = ORMFavoriteProductsIdsService()
        self.get_all_products_service = ORMAllProductsService()
        self.products_service = ORMFavoriteProductsIdsFilterService()

        self.command_handler = FavoritePageCommandHandler(
            favorite_products_service_ids=self.favorite_products_service_ids,
            get_all_products_service=self.get_all_products_service,
            products_service=self.products_service,
        )

    def test_handle_unauthenticated_user(self):
        command = FavoritePageCommand(is_authenticated=False)

        response = self.command_handler.handle(command)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, DTOResponseFavoriteAPI)
        self.assertEqual(response.products, [])

    def test_handle_user_with_no_favorites(self):
        command = FavoritePageCommand(is_authenticated=True, username="test_user")

        response = self.command_handler.handle(command)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, DTOResponseFavoriteAPI)
        self.assertEqual(response.products, [])

    def test_handle_user_with_favorites(self):
        command = FavoritePageCommand(is_authenticated=True, username="test_user")

        Favorites.objects.create(user=self.user, product_id=self.product_1.id)
        Favorites.objects.create(user=self.user, product_id=self.product_2.id)

        all_products = [
            {"id": self.product_1.id, "title": "Product 1"},
            {"id": self.product_2.id, "title": "Product 2"},
            {"id": 4, "title": "Product 4"},
        ]

        self.get_all_products_service.get_all_products = lambda: all_products

        filtered_products = [
            {"id": self.product_1.id, "title": "Product 1"},
            {"id": self.product_2.id, "title": "Product 2"},
        ]

        self.products_service.get_filtered_products_by_favorite_ids = (
            lambda products, ids_products_in_favorite: filtered_products
        )

        response = self.command_handler.handle(command)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, DTOResponseFavoriteAPI)
        self.assertEqual(response.products, filtered_products)
