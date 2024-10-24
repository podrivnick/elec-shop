import unittest
from unittest.mock import MagicMock

from core.apps.carts_products.exceptions.main import (
    ProductNotFoundError,
    ReviewNotFoundError,
    UserAlreadyWriteReviewError,
)
from core.apps.carts_products.use_cases.reviews import (
    ChangeLikesReviewCommand,
    ChangeLikesReviewCommandHandler,
    CreateReviewCommand,
    CreateReviewCommandHandler,
    DeleteReviewCommand,
    DeleteReviewCommandHandler,
)
from core.apps.common.exceptions.main import (
    AuthenticationError,
    UserNotFoundByUsername,
)
from core.apps.packet.exceptions.main import DatabaseCartError


class TestCreateReviewCommandHandler(unittest.TestCase):
    def setUp(self):
        self.query_get_user_model_by_username = MagicMock()
        self.query_get_review_service = MagicMock()
        self.query_product_repository = MagicMock()
        self.command_update_review_service = MagicMock()

        self.handler = CreateReviewCommandHandler(
            query_get_user_model_by_username=self.query_get_user_model_by_username,
            query_get_review_service=self.query_get_review_service,
            query_product_repository=self.query_product_repository,
            command_update_review_service=self.command_update_review_service,
        )

    def test_handle_with_authenticated_user_and_no_existing_review(self):
        command = CreateReviewCommand(
            is_authenticated=True,
            username="testuser",
            product_slug="test-product-slug",
            id_product=1,
            review="Great product!",
        )

        user_model = MagicMock()
        product_model = [MagicMock()]

        self.query_get_user_model_by_username.get_usermodel_by_username.return_value = (
            user_model
        )
        self.query_get_review_service.get_review_product_by_user.return_value = (
            None  # Нет существующего отзыва
        )
        self.query_product_repository.filter_product_by_slug.return_value = (
            product_model
        )

        response = self.handler.handle(command)

        self.query_get_user_model_by_username.get_usermodel_by_username.assert_called_once_with(
            username="testuser",
        )
        self.query_get_review_service.get_review_product_by_user.assert_called_once_with(
            id_product=1,
            user=user_model,
        )
        self.query_product_repository.filter_product_by_slug.assert_called_once_with(
            slug="test-product-slug",
        )
        self.command_update_review_service.create_review_product.assert_called_once_with(
            product_object=product_model[0],
            user=user_model,
            review="Great product!",
        )

        self.assertEqual(response.product_slug, "test-product-slug")

    def test_handle_with_unauthenticated_user(self):
        command = CreateReviewCommand(
            is_authenticated=False,
            username="testuser",
            product_slug="test-product-slug",
            id_product=1,
            review="Great product!",
        )

        with self.assertRaises(AuthenticationError):
            self.handler.handle(command)

    def test_handle_with_existing_review(self):
        command = CreateReviewCommand(
            is_authenticated=True,
            username="testuser",
            product_slug="test-product-slug",
            id_product=1,
            review="Great product!",
        )

        user_model = MagicMock()
        reviews_entity = MagicMock()

        self.query_get_user_model_by_username.get_usermodel_by_username.return_value = (
            user_model
        )
        self.query_get_review_service.get_review_product_by_user.return_value = (
            reviews_entity
        )

        with self.assertRaises(UserAlreadyWriteReviewError):
            self.handler.handle(command)

    def test_handle_with_database_error(self):
        command = CreateReviewCommand(
            is_authenticated=True,
            username="testuser",
            product_slug="test-product-slug",
            id_product=1,
            review="Great product!",
        )

        user_model = MagicMock()
        product_model = [MagicMock()]

        self.query_get_user_model_by_username.get_usermodel_by_username.return_value = (
            user_model
        )
        self.query_get_review_service.get_review_product_by_user.return_value = None
        self.query_product_repository.filter_product_by_slug.return_value = (
            product_model
        )

        self.command_update_review_service.create_review_product.side_effect = (
            Exception("DB error")
        )

        with self.assertRaises(DatabaseCartError):
            self.handler.handle(command)


class TestChangeLikesReviewCommandHandler(unittest.TestCase):
    def setUp(self):
        self.query_get_user_model_by_username = MagicMock()
        self.query_product_repository = MagicMock()
        self.query_get_review_service = MagicMock()
        self.query_like_review_service = MagicMock()
        self.command_likes_review_service = MagicMock()

        self.handler = ChangeLikesReviewCommandHandler(
            query_get_user_model_by_username=self.query_get_user_model_by_username,
            query_product_repository=self.query_product_repository,
            query_get_review_service=self.query_get_review_service,
            query_like_review_service=self.query_like_review_service,
            command_likes_review_service=self.command_likes_review_service,
        )

    def test_handle_with_authenticated_user_and_valid_data(self):
        command = ChangeLikesReviewCommand(
            is_authenticated=True,
            username="testuser",
            product_id="123",
            review_id=1,
        )

        user_model = MagicMock()
        product_model = MagicMock()
        review = MagicMock()
        liked_review = MagicMock()
        updated_likes = MagicMock()

        self.query_get_user_model_by_username.get_usermodel_by_username.return_value = (
            user_model
        )
        self.query_product_repository.get_product_by_id.return_value = product_model
        self.query_get_review_service.get_review_by_product_model.return_value = review
        self.query_like_review_service.filter_likes_by_review_product.return_value = (
            liked_review
        )
        self.command_likes_review_service.update_likes_review.return_value = (
            updated_likes
        )

        response = self.handler.handle(command)

        self.query_get_user_model_by_username.get_usermodel_by_username.assert_called_once_with(
            username="testuser",
        )
        self.query_product_repository.get_product_by_id.assert_called_once_with(
            id_product="123",
        )
        self.query_get_review_service.get_review_by_product_model.assert_called_once_with(
            product=product_model,
            review_id=1,
        )
        self.query_like_review_service.filter_likes_by_review_product.assert_called_once_with(
            user=user_model,
            product=product_model,
            review=review,
        )
        self.command_likes_review_service.update_likes_review.assert_called_once_with(
            likes_model=liked_review,
            product=product_model,
            user=user_model,
            review=review,
        )

        self.assertEqual(response.updated_likes, updated_likes)

    def test_handle_with_unauthenticated_user(self):
        command = ChangeLikesReviewCommand(
            is_authenticated=False,
            username="testuser",
            product_id="123",
            review_id=1,
        )

        with self.assertRaises(AuthenticationError):
            self.handler.handle(command)

    def test_handle_with_non_existent_product(self):
        command = ChangeLikesReviewCommand(
            is_authenticated=True,
            username="testuser",
            product_id="invalid",
            review_id=1,
        )

        user_model = MagicMock()

        self.query_get_user_model_by_username.get_usermodel_by_username.return_value = (
            user_model
        )
        self.query_product_repository.get_product_by_id.return_value = (
            None  # Продукт не найден
        )

        with self.assertRaises(ProductNotFoundError):
            self.handler.handle(command)

    def test_handle_with_non_existent_review(self):
        command = ChangeLikesReviewCommand(
            is_authenticated=True,
            username="testuser",
            product_id="123",
            review_id=999,
        )

        user_model = MagicMock()
        product_model = MagicMock()

        self.query_get_user_model_by_username.get_usermodel_by_username.return_value = (
            user_model
        )
        self.query_product_repository.get_product_by_id.return_value = product_model
        self.query_get_review_service.get_review_by_product_model.return_value = None

        with self.assertRaises(ReviewNotFoundError):
            self.handler.handle(command)


class TestDeleteReviewCommandHandler(unittest.TestCase):
    def setUp(self):
        self.query_get_user_model_by_username = MagicMock()
        self.command_review_service = MagicMock()

        self.handler = DeleteReviewCommandHandler(
            query_get_user_model_by_username=self.query_get_user_model_by_username,
            command_review_service=self.command_review_service,
        )

    def test_handle_with_authenticated_user_and_valid_data(self):
        command = DeleteReviewCommand(
            is_authenticated=True,
            username="testuser",
            slug_product="test-product",
            pk_product=123,
        )

        user_model = MagicMock()

        self.query_get_user_model_by_username.get_usermodel_by_username.return_value = (
            user_model
        )

        response = self.handler.handle(command)

        self.query_get_user_model_by_username.get_usermodel_by_username.assert_called_once_with(
            username="testuser",
        )
        self.command_review_service.delete_review_product.assert_called_once_with(
            user=user_model,
            pk_product=123,
        )

        self.assertEqual(response.slug_product, "test-product")

    def test_handle_with_unauthenticated_user(self):
        command = DeleteReviewCommand(
            is_authenticated=False,
            username="testuser",
            slug_product="test-product",
            pk_product=123,
        )

        with self.assertRaises(AuthenticationError):
            self.handler.handle(command)

    def test_handle_with_non_existent_user(self):
        command = DeleteReviewCommand(
            is_authenticated=True,
            username="nonexistent_user",
            slug_product="test-product",
            pk_product=123,
        )

        self.query_get_user_model_by_username.get_usermodel_by_username.return_value = (
            None
        )

        with self.assertRaises(UserNotFoundByUsername):
            self.handler.handle(command)

    def test_handle_with_invalid_pk_product(self):
        command = DeleteReviewCommand(
            is_authenticated=True,
            username="testuser",
            slug_product="test-product",
            pk_product=None,
        )

        user_model = MagicMock()

        self.query_get_user_model_by_username.get_usermodel_by_username.return_value = (
            user_model
        )

        with self.assertRaises(ValueError):
            self.handler.handle(command)
