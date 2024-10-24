import unittest
from datetime import datetime
from unittest.mock import MagicMock

import pytest

from core.api.v1.carts_products.dto.responses import DTOResponseCartAPI
from core.apps.carts_products.entities.review import ReviewEntity
from core.apps.carts_products.schemas.main import ReviewDataSchema
from core.apps.carts_products.use_cases.cart import (
    CartPageCommand,
    CartPageCommandHandler,
    ReviewsPageCommand,
    ReviewsPageCommandHandler,
)
from core.apps.main.entities.product import ProductEntity
from core.apps.users.models import User


@pytest.fixture
def create_user(db):
    # ORM
    return User.objects.create_user(
        username="test_user",
        email="test_user@example.com",
        password="testpassword123",
    )


@pytest.fixture
def setup_command_handler():
    # Mocks
    query_products_service = MagicMock()
    query_reviews_filtered_service = MagicMock()
    query_favorite_products_service_ids = MagicMock()
    query_likes_filter_service = MagicMock()
    query_get_user_model_by_username = MagicMock()

    return CartPageCommandHandler(
        query_products_service=query_products_service,
        query_reviews_filtered_service=query_reviews_filtered_service,
        query_favorite_products_service_ids=query_favorite_products_service_ids,
        query_likes_filter_service=query_likes_filter_service,
        query_get_user_model_by_username=query_get_user_model_by_username,
    )


@pytest.fixture
def setup_command():
    return CartPageCommand(
        is_authenticated=True,
        username="test_user",
        product_slug="test-product-slug",
    )


def test_handle_authenticated_user(setup_command_handler, setup_command, create_user):
    product_entity = ProductEntity(
        id_product=1,
        slug="test-product-slug",
        name="some",
        description="some descriprion",
        image="some/product",
        discount=0,
        price=2000,
        count_product=30,
        category="all",
        created_at=datetime(2024, 10, 10, 14, 30, 45),
        updated_at=datetime(2024, 10, 10, 14, 30, 45),
    )

    setup_command_handler.query_products_service.get_filtered_product_by_slug.return_value = product_entity

    reviews = [
        ReviewEntity(
            pk=1,
            data_added=datetime(2024, 10, 10, 14, 30, 45),
            user=create_user,
        ),
        ReviewEntity(
            pk=2,
            data_added=datetime(2024, 10, 10, 14, 30, 45),
            user=create_user,
        ),
    ]
    setup_command_handler.query_reviews_filtered_service.get_reviews_product.return_value = reviews

    # Мок фаворитов
    setup_command_handler.query_favorite_products_service_ids.get_ids_products_in_favorite.return_value = [
        1,
        2,
    ]

    user = MagicMock()
    setup_command_handler.query_get_user_model_by_username.get_usermodel_by_username.return_value = user

    setup_command_handler.query_likes_filter_service.get_liked_review.return_value = [
        reviews[0],
    ]
    setup_command_handler.query_likes_filter_service.filter_reviews_by_user.return_value = reviews

    result = setup_command_handler.handle(setup_command)

    assert isinstance(result, DTOResponseCartAPI)
    assert result.products == product_entity
    assert result.favorites == [1, 2]
    assert result.count_all_reviews == len(reviews)
    assert result.liked_objects == [reviews[0]]
    assert result.reviews == reviews
    assert isinstance(result.form, ReviewDataSchema)

    setup_command_handler.query_products_service.get_filtered_product_by_slug.assert_called_once_with(
        slug="test-product-slug",
    )
    setup_command_handler.query_reviews_filtered_service.get_reviews_product.assert_called_once_with(
        id_product=product_entity.id_product,
    )
    setup_command_handler.query_favorite_products_service_ids.get_ids_products_in_favorite.assert_called_once_with(
        username="test_user",
    )
    setup_command_handler.query_get_user_model_by_username.get_usermodel_by_username.assert_called_once_with(
        username="test_user",
    )
    setup_command_handler.query_likes_filter_service.get_liked_review.assert_called_once_with(
        user=user,
        id_product=product_entity.id_product,
        reviews=reviews,
    )
    setup_command_handler.query_likes_filter_service.filter_reviews_by_user.assert_called_once_with(
        user=user,
        reviews=reviews,
    )


class TestReviewsPageCommandHandler(unittest.TestCase):
    def setUp(self):
        # Создаем моковые сервисы
        self.query_products_service = MagicMock()
        self.query_reviews_filtered_service = MagicMock()
        self.query_likes_filter_service = MagicMock()
        self.query_get_user_model_by_username = MagicMock()

        # Инициализация хендлера с моками
        self.handler = ReviewsPageCommandHandler(
            query_products_service=self.query_products_service,
            query_reviews_filtered_service=self.query_reviews_filtered_service,
            query_likes_filter_service=self.query_likes_filter_service,
            query_get_user_model_by_username=self.query_get_user_model_by_username,
        )

    def test_handle_with_authenticated_user(self):
        # Подготовка данных
        command = ReviewsPageCommand(
            is_authenticated=True,
            username="testuser",
            product_slug="test-product-slug",
        )

        product_entity = ProductEntity(
            id_product=1,
            slug="test-product-slug",
            name="some",
            description="some descriprion",
            image="some/product",
            discount=0,
            price=2000,
            count_product=30,
            category="all",
            created_at=datetime(2024, 10, 10, 14, 30, 45),
            updated_at=datetime(2024, 10, 10, 14, 30, 45),
        )
        review_entity = ReviewEntity(pk=1, data_added="2024-10-17", user="testuser")

        self.query_products_service.get_filtered_product_by_slug.return_value = (
            product_entity
        )
        self.query_reviews_filtered_service.get_reviews_product.return_value = [
            review_entity,
        ]
        self.query_get_user_model_by_username.get_usermodel_by_username.return_value = (
            "testuser"
        )
        self.query_likes_filter_service.get_liked_review.return_value = ["liked_review"]
        self.query_likes_filter_service.filter_reviews_by_user.return_value = [
            review_entity,
        ]

        response = self.handler.handle(command)

        self.query_products_service.get_filtered_product_by_slug.assert_called_once_with(
            slug="test-product-slug",
        )
        self.query_reviews_filtered_service.get_reviews_product.assert_called_once_with(
            id_product=1,
        )
        self.query_get_user_model_by_username.get_usermodel_by_username.assert_called_once_with(
            username="testuser",
        )
        self.query_likes_filter_service.get_liked_review.assert_called_once_with(
            user="testuser",
            id_product=1,
            reviews=[review_entity],
        )
        self.query_likes_filter_service.filter_reviews_by_user.assert_called_once_with(
            user="testuser",
            reviews=[review_entity],
        )

        self.assertEqual(response.product, product_entity)
        self.assertEqual(response.liked_objects, ["liked_review"])
        self.assertEqual(response.reviews, [review_entity])

    def test_handle_with_unauthenticated_user(self):
        command = ReviewsPageCommand(
            is_authenticated=False,
            username=None,
            product_slug="test-product-slug",
        )

        product_entity = ProductEntity(
            id_product=1,
            slug="test-product-slug",
            name="some",
            description="some descriprion",
            image="some/product",
            discount=0,
            price=2000,
            count_product=30,
            category="all",
            created_at=datetime(2024, 10, 10, 14, 30, 45),
            updated_at=datetime(2024, 10, 10, 14, 30, 45),
        )
        review_entity = ReviewEntity(pk=1, data_added="2024-10-17", user="testuser")

        self.query_products_service.get_filtered_product_by_slug.return_value = (
            product_entity
        )
        self.query_reviews_filtered_service.get_reviews_product.return_value = [
            review_entity,
        ]

        response = self.handler.handle(command)

        self.query_products_service.get_filtered_product_by_slug.assert_called_once_with(
            slug="test-product-slug",
        )
        self.query_reviews_filtered_service.get_reviews_product.assert_called_once_with(
            id_product=1,
        )

        self.query_get_user_model_by_username.get_usermodel_by_username.assert_not_called()
        self.query_likes_filter_service.get_liked_review.assert_not_called()
        self.query_likes_filter_service.filter_reviews_by_user.assert_not_called()

        self.assertEqual(response.product, product_entity)
        self.assertEqual(response.liked_objects, [])
        self.assertEqual(response.reviews, [review_entity])
