from dataclasses import dataclass

from core.apps.main.models.favorites import Favorites
from core.apps.main.services.update_favorite.base import (
    BaseCommandUpdateFavoriteProductsService,
    BaseQueryUpdateFavoriteProductsService,
)


@dataclass
class ORMQueryUpdateFavoriteProductsService(BaseQueryUpdateFavoriteProductsService):
    def check_product_in_favorite_is_exist(
        self,
        username: str,
        product_id: int,
    ) -> bool:
        is_product_in_favorite = Favorites.objects.filter(
            user__username=username,
            product_id=product_id,
        ).exists()

        return is_product_in_favorite


@dataclass
class ORMCommandUpdateFavoriteProductsService(BaseCommandUpdateFavoriteProductsService):
    def add_product_to_favorite(
        self,
        user: str,
        product_id: int,
    ) -> None:
        Favorites.objects.create(user=user, product_id=product_id)

    def delete_product_from_favorite(
        self,
        username: str,
        product_id: int,
    ) -> None:
        Favorites.objects.filter(
            user__username=username,
            product_id=product_id,
        ).delete()
