from dataclasses import dataclass
from typing import Union

from django.db.models import QuerySet

from .models import Favorites, Products
from .utils import GetUserModel, q_search


@dataclass
class SaveFavoriteService:
    data: dict

    def save_favorite_service(self):
        username = self.data['data'][0]
        product_id = self.data['data'][1]

        get_user = GetUserModel(username)
        user = get_user.get_user_model()

        is_product_in_favorite = Favorites.objects.filter(user=user, product_id=product_id).exists()

        if is_product_in_favorite:
            Favorites.objects.filter(user=user, product_id=product_id).delete()
        else:
            Favorites.objects.create(user=user, product_id=product_id)


@dataclass
class CreateFavoritePage:
    username: str
    products: Union[Products, QuerySet[Products]]

    def create_data_for_favorite_page(self):
        get_user = GetUserModel(self.username)
        user = get_user.get_user_model()

        favorites = Favorites.objects.filter(user=user)
        products_id = [item.product_id for item in favorites]

        if self.products:
            filter_products_by_favorite = self.products.filter(id_product__in=products_id)

            return filter_products_by_favorite
        else:
            return products_id


@dataclass
class FilterProductsBySortingCategoriesSearch:
    is_available: bool
    is_discount: bool
    is_sorting: str
    slug: str
    query: str
    products: Union[Products, QuerySet[Products]]

    def make_filters(self):
        is_search_failed = False

        if self.is_available:
            self.products = self.products.filter(count_product__gt=0)

        if self.is_discount:
            self.products = self.products.filter(discount__gt=0)

        if self.is_sorting and self.is_sorting != 'default':
            self.products = self.products.order_by(self.is_sorting)

        if self.slug and self.slug != 'all':
            self.products = self.products.filter(category__slug=self.slug)

        if self.query:
            self.products = q_search(self.query, self.products)

            if not len(self.products):
                is_search_failed = True

        return is_search_failed, self.products


