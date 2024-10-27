from functools import lru_cache
from core.apps.main.use_cases.update_favorite import (
    UpdateFavoritePageCommand,
    UpdateFavoritePageCommandHandler,
)
from core.apps.main.use_cases.info import (
    InformationPageCommand,
    InformationPageCommandHandler,
)
from core.apps.users.services.profile.main import QueryValidateNewDataService
from core.apps.users.services.profile.main import (
    ORMCommandSetUpdatedInformationOfUserService,
)
from punq import Container
from core.apps.common.services.main import ORMQueryGetUserModelService
from core.apps.main.services.favorites.favorites import (
    ORMFavoriteProductsIdsFilterService,
)
from core.apps.main.services.main.main import (
    ORMCategoriesService,
    ORMProductsService,
)
from core.apps.main.services.universal import (
    ORMAllProductsService,
    ORMFavoriteProductsIdsService,
)
from core.apps.main.use_cases.favorite import (
    FavoritePageCommand,
    FavoritePageCommandHandler,
)
from core.apps.main.use_cases.main import (
    MainPageCommand,
    MainPageCommandHandler,
)
from core.apps.main.services.information.main import ORMQueryFAQInformationService
from core.infrastructure.mediator.mediator import Mediator
from core.apps.main.services.update_favorite.main import (
    ORMCommandUpdateFavoriteProductsService,
    ORMQueryUpdateFavoriteProductsService,
)
from punq import (
    Scope,
)
from core.apps.users.use_cases.login import (
    AuthenticatePageCommandHandler,
    AuthenticatePageCommand,
)
from core.apps.users.use_cases.logout import LogoutCommandHandler, LogoutCommand
from core.apps.users.services.login.main import (
    ORMCommandVerificateUserService,
    ORMCommandAuthenticateUserService,
    ORMCommandAddPacketToUserBySessionKeyService,
)
from core.apps.users.services.registration.main import (
    ORMQueryUserInNotExistService,
    ORMCommandCreateUserService,
)
from core.apps.users.use_cases.registration import (
    RegistrationPageCommand,
    RegistrationPageCommandHandler,
)
from core.apps.users.use_cases.registration import (
    RegisterCommandHandler,
    RegisterCommand,
)
from core.apps.packet.services.base import BaseCommandUpdateDataCartService
from core.apps.users.use_cases.login import LoginPageCommand, LoginPageCommandHandler
from core.apps.users.services.logout.main import ORMCommandLogoutUserService
from core.apps.users.use_cases.profile import (
    ProfilePageCommand,
    ProfilePageCommandHandler,
    ProfileCommand,
    ProfileCommandHandler,
)
from core.apps.carts_products.services.main import (
    ORMQueryLikesReviewService,
    ORMQueryGetReviewsService,
)
from core.apps.carts_products.use_cases.cart import (
    CartPageCommand,
    CartPageCommandHandler,
)
from core.apps.carts_products.use_cases.cart import (
    ReviewsPageCommandHandler,
    ReviewsPageCommand,
)
from core.apps.carts_products.services.base import (
    BaseQueryGetReviewsService,
    BaseQueryLikesReviewService,
)
from core.apps.users.services.profile.main import ORMQueryFilterCartsByUserService
from core.apps.users.use_cases.profile import ChangeTabCommandHandler, ChangeTabCommand
from core.apps.packet.repositories.main import ORMCommandUpdateCartRepository
from core.apps.packet.services.main import (
    CommandUpdateDataCartService,
    ORMQueryGetCartService,
    ORMQueryGetProductService,
)
from core.apps.packet.use_cases.packet import (
    ChangePacketCommandHandler,
    ChangePacketCommand,
)
from core.apps.packet.use_cases.packet import (
    DeletePacketCommand,
    DeletePacketCommandHandler,
)
from core.apps.main.services.main.base import (
    BaseProductsService,
)
from core.apps.carts_products.repositories.main import ORMQueryLikeReviewsRepository
from core.apps.packet.use_cases.packet import AddPacketCommandHandler, AddPacketCommand
from core.apps.main.repositories.main import ORMQueryProductRepository
from core.apps.carts_products.use_cases.reviews import (
    CreateReviewCommandHandler,
    CreateReviewCommand,
)
from core.apps.carts_products.services.base import BaseCommandLikesReviewService
from core.apps.carts_products.repositories.main import ORMCommandLikeReviewsRepository
from core.apps.carts_products.services.main import ORMCommandLikesReviewService
from core.apps.carts_products.services.main import ORMCommandReviewsService
from core.apps.carts_products.use_cases.reviews import (
    ChangeLikesReviewCommandHandler,
    ChangeLikesReviewCommand,
)
from core.apps.carts_products.use_cases.reviews import (
    DeleteReviewCommandHandler,
    DeleteReviewCommand,
)
from core.apps.carts_products.use_cases.finalize import (
    FinalizePageCommandHandler,
    FinalizePageCommand,
)
from core.apps.orders.use_cases.order import OrderCommandHandler, OrderCommand
from core.apps.orders.services.order import (
    QueryValidationOrderService,
    ORMBaseCommandOrderService,
)
from core.apps.orders.repositories.order import ORMBaseCommandOrderRepository
from core.apps.orders.services.order import BaseCommandOrderService


@lru_cache(1)
def init_container() -> Container:
    return _initialize_container()


def _initialize_container() -> Container:
    container = Container()

    # init services
    def init_update_packet_service() -> BaseCommandUpdateDataCartService:
        return CommandUpdateDataCartService(
            command_update_cart=ORMCommandUpdateCartRepository(),
        )

    def init_likes_review_service() -> BaseQueryLikesReviewService:
        return ORMQueryLikesReviewService(
            query_filter_likes_review_repository=ORMQueryLikeReviewsRepository(),
        )

    def init_reviews_service() -> BaseQueryGetReviewsService:
        return ORMQueryGetReviewsService(
            query_filter_likes_review_repository=ORMQueryLikeReviewsRepository(),
        )

    def init_product_service() -> BaseProductsService:
        return ORMProductsService(
            query_product_repository=ORMQueryProductRepository(),
        )

    def init_command_like_review_service() -> BaseCommandLikesReviewService:
        return ORMCommandLikesReviewService(
            command_likes_review_repository=ORMCommandLikeReviewsRepository(),
        )

    def init_command_order_service() -> BaseCommandOrderService:
        return ORMBaseCommandOrderService(
            command_create_orders_item_repository=ORMBaseCommandOrderRepository(),
        )

    container.register(
        BaseCommandOrderService,
        factory=init_command_order_service,
        scope=Scope.singleton,
    )

    container.register(
        BaseCommandUpdateDataCartService,
        factory=init_update_packet_service,
        scope=Scope.singleton,
    )

    container.register(
        BaseCommandLikesReviewService,
        factory=init_command_like_review_service,
        scope=Scope.singleton,
    )

    container.register(
        BaseQueryGetReviewsService,
        factory=init_reviews_service,
        scope=Scope.singleton,
    )

    container.register(
        BaseQueryLikesReviewService,
        factory=init_likes_review_service,
        scope=Scope.singleton,
    )

    container.register(
        BaseProductsService,
        factory=init_product_service,
        scope=Scope.singleton,
    )

    # Handlers
    container.register(MainPageCommandHandler)
    container.register(FavoritePageCommandHandler)
    container.register(UpdateFavoritePageCommandHandler)
    container.register(InformationPageCommandHandler)
    container.register(LoginPageCommandHandler)
    container.register(AuthenticatePageCommandHandler)
    container.register(LogoutCommandHandler)
    container.register(RegistrationPageCommandHandler)
    container.register(RegisterCommandHandler)
    container.register(ProfilePageCommandHandler)
    container.register(ProfileCommandHandler)
    container.register(ChangeTabCommandHandler)
    container.register(AddPacketCommandHandler)
    container.register(DeletePacketCommandHandler)
    container.register(ChangePacketCommandHandler)
    container.register(CartPageCommandHandler)
    container.register(ReviewsPageCommandHandler)
    container.register(CreateReviewCommandHandler)
    container.register(ChangeLikesReviewCommandHandler)
    container.register(DeleteReviewCommandHandler)
    container.register(FinalizePageCommandHandler)
    container.register(OrderCommandHandler)

    def init_mediator() -> Mediator:
        mediator = Mediator()

        # command handlers
        # main app
        configure_main_page_handler = MainPageCommandHandler(
            favorite_products_service_ids=ORMFavoriteProductsIdsService(),
            get_all_products_service=ORMAllProductsService(),
            categories_service=ORMCategoriesService(),
            products_service=container.resolve(
                BaseProductsService,
            ),
        )

        configure_favorite_page_handler = FavoritePageCommandHandler(
            favorite_products_service_ids=ORMFavoriteProductsIdsService(),
            get_all_products_service=ORMAllProductsService(),
            products_service=ORMFavoriteProductsIdsFilterService(),
        )

        configure_update_favorite_products_handler = UpdateFavoritePageCommandHandler(
            query_get_user_model_by_username=ORMQueryGetUserModelService(),
            query_update_favorite_product_service=ORMQueryUpdateFavoriteProductsService(),
            command_update_favorite_product_service=ORMCommandUpdateFavoriteProductsService(),
        )

        configure_information_page_handler = InformationPageCommandHandler(
            query_get_all_information=ORMQueryFAQInformationService(),
        )

        # user app
        configure_login_page_handler = LoginPageCommandHandler()

        configure_authentice_handler = AuthenticatePageCommandHandler(
            command_verificate_password_service=ORMCommandVerificateUserService(),
            command_authenticate_user_service=ORMCommandAuthenticateUserService(),
            command_add_packet_to_user_by_session_key=ORMCommandAddPacketToUserBySessionKeyService(),
        )

        configure_logout_handler = LogoutCommandHandler(
            command_logout_user_service=ORMCommandLogoutUserService(),
        )

        configure_registration_handler = RegistrationPageCommandHandler()

        configure_register_handler = RegisterCommandHandler(
            query_verificate_user_is_not_exist=ORMQueryUserInNotExistService(),
            command_create_user_by_enter_data=ORMCommandCreateUserService(),
            command_authenticate_user_service=ORMCommandAuthenticateUserService(),
            command_add_packet_to_user_by_session_key=ORMCommandAddPacketToUserBySessionKeyService(),
        )

        configure_profile_page_handler = ProfilePageCommandHandler(
            query_filter_carts_by_user=ORMQueryFilterCartsByUserService(),
            query_validate_new_information=QueryValidateNewDataService(),
            query_get_user_model=ORMQueryGetUserModelService(),
            command_set_updated_information_of_user=ORMCommandSetUpdatedInformationOfUserService(),
        )

        configure_profile_handler = ProfileCommandHandler(
            query_validate_new_information=QueryValidateNewDataService(),
            query_get_user_model=ORMQueryGetUserModelService(),
            command_set_updated_information_of_user=ORMCommandSetUpdatedInformationOfUserService(),
        )

        configure_change_tab_handler = ChangeTabCommandHandler()

        # packet app
        configure_add_packet_handler = AddPacketCommandHandler(
            query_get_user_model=ORMQueryGetUserModelService(),
            query_get_product_by_id=ORMQueryGetProductService(),
            query_get_cart_by_product_and_user=ORMQueryGetCartService(),
            command_update_or_create_cart=container.resolve(
                BaseCommandUpdateDataCartService,
            ),
        )

        configure_delete_packet_handler = DeletePacketCommandHandler(
            command_delete_cart_from_packet=container.resolve(
                BaseCommandUpdateDataCartService,
            ),
            query_get_user_model=ORMQueryGetUserModelService(),
            query_get_cart_by_user=ORMQueryGetCartService(),
        )

        configure_change_packet_handler = ChangePacketCommandHandler(
            command_change_quantity_cart_from_packet=container.resolve(
                BaseCommandUpdateDataCartService,
            ),
            query_get_user_model=ORMQueryGetUserModelService(),
            query_get_cart=ORMQueryGetCartService(),
        )

        # cart app
        configure_cart_page_handler = CartPageCommandHandler(
            query_products_service=container.resolve(
                BaseProductsService,
            ),
            query_reviews_filtered_service=container.resolve(
                BaseQueryGetReviewsService,
            ),
            query_favorite_products_service_ids=ORMFavoriteProductsIdsService(),
            query_likes_filter_service=container.resolve(
                BaseQueryLikesReviewService,
            ),
            query_get_user_model_by_username=ORMQueryGetUserModelService(),
        )

        configure_reviews_page_handler = ReviewsPageCommandHandler(
            query_products_service=container.resolve(
                BaseProductsService,
            ),
            query_reviews_filtered_service=container.resolve(
                BaseQueryGetReviewsService,
            ),
            query_likes_filter_service=container.resolve(
                BaseQueryLikesReviewService,
            ),
            query_get_user_model_by_username=ORMQueryGetUserModelService(),
        )

        configure_create_reviews_handler = CreateReviewCommandHandler(
            query_get_user_model_by_username=ORMQueryGetUserModelService(),
            query_get_review_service=container.resolve(
                BaseQueryGetReviewsService,
            ),
            query_product_repository=ORMQueryProductRepository(),
            command_update_review_service=ORMCommandReviewsService(),
        )

        configure_change_likes_reviews_handler = ChangeLikesReviewCommandHandler(
            query_get_user_model_by_username=ORMQueryGetUserModelService(),
            query_product_repository=ORMQueryProductRepository(),
            query_get_review_service=container.resolve(
                BaseQueryGetReviewsService,
            ),
            query_like_review_service=container.resolve(
                BaseQueryLikesReviewService,
            ),
            command_likes_review_service=container.resolve(
                BaseCommandLikesReviewService,
            ),
        )

        configure_delete_reviews_handler = DeleteReviewCommandHandler(
            query_get_user_model_by_username=ORMQueryGetUserModelService(),
            command_review_service=ORMCommandReviewsService(),
        )

        configure_finalize_handler = FinalizePageCommandHandler(
            query_get_user_model_by_username=ORMQueryGetUserModelService(),
            query_get_carts_service=ORMQueryGetCartService(),
        )

        # order app
        configure_order_handler = OrderCommandHandler(
            query_get_user_model_by_username=ORMQueryGetUserModelService(),
            query_validation_order_data_service=QueryValidationOrderService(),
            command_create_basic_order=container.resolve(
                BaseCommandOrderService,
            ),
            query_filter_packet_service=ORMQueryGetCartService(),
            command_order_repository=ORMBaseCommandOrderRepository(),
        )

        # commands
        # main app
        mediator.register_command(
            MainPageCommand,
            [configure_main_page_handler],
        )

        mediator.register_command(
            FavoritePageCommand,
            [configure_favorite_page_handler],
        )

        mediator.register_command(
            UpdateFavoritePageCommand,
            [configure_update_favorite_products_handler],
        )

        mediator.register_command(
            InformationPageCommand,
            [configure_information_page_handler],
        )

        # user app
        mediator.register_command(
            LoginPageCommand,
            [configure_login_page_handler],
        )

        mediator.register_command(
            AuthenticatePageCommand,
            [configure_authentice_handler],
        )

        mediator.register_command(
            LogoutCommand,
            [configure_logout_handler],
        )

        mediator.register_command(
            RegistrationPageCommand,
            [configure_registration_handler],
        )

        mediator.register_command(
            RegisterCommand,
            [configure_register_handler],
        )

        mediator.register_command(
            ProfilePageCommand,
            [configure_profile_page_handler],
        )

        mediator.register_command(
            ProfileCommand,
            [configure_profile_handler],
        )

        mediator.register_command(
            ChangeTabCommand,
            [configure_change_tab_handler],
        )

        # packet app
        mediator.register_command(
            AddPacketCommand,
            [configure_add_packet_handler],
        )

        mediator.register_command(
            DeletePacketCommand,
            [configure_delete_packet_handler],
        )

        mediator.register_command(
            ChangePacketCommand,
            [configure_change_packet_handler],
        )

        # cart app
        mediator.register_command(
            CartPageCommand,
            [configure_cart_page_handler],
        )

        mediator.register_command(
            ReviewsPageCommand,
            [configure_reviews_page_handler],
        )

        mediator.register_command(
            CreateReviewCommand,
            [configure_create_reviews_handler],
        )

        mediator.register_command(
            ChangeLikesReviewCommand,
            [configure_change_likes_reviews_handler],
        )

        mediator.register_command(
            DeleteReviewCommand,
            [configure_delete_reviews_handler],
        )

        mediator.register_command(
            FinalizePageCommand,
            [configure_finalize_handler],
        )

        mediator.register_command(
            OrderCommand,
            [configure_order_handler],
        )

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
