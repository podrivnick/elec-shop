import json

from django.http import JsonResponse
from django.views.generic import ListView
from django.views import View
from django.views.generic import TemplateView

from .models import Information, Products, Categories_Product
from .services import SaveFavoriteService, CreateFavoritePage, FilterProductsBySortingCategoriesSearch


class MainPage(ListView):
    template_name = "main_favorite/index.html"
    model = Products
    context_object_name = 'products'
    slug_url_kwarg = 'category_slug'
    paginate_by = 6

    def get_context_data(self, *, object_list=None,  **kwargs):
        context = super().get_context_data(**kwargs)

        categories = Categories_Product.objects.all()
        if self.request.user.is_authenticated:
            username = self.request.user.username

            get_product_in_favorite = CreateFavoritePage(username, False)

            context['favorites'] = get_product_in_favorite.create_data_for_favorite_page()

        context['is_search_failed'] = getattr(self, 'is_search_failed')
        context['categories'] = categories

        return dict(list(context.items()))

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()

        is_available = self.request.GET.get('available')
        is_discount = self.request.GET.get('discount')
        is_sorting = self.request.GET.get('sorting')

        slug = self.kwargs.get('category_slug')
        query = self.request.GET.get('search', None)

        make_filters_products = FilterProductsBySortingCategoriesSearch(
            is_available, is_discount, is_sorting,
            slug, query, queryset
        )

        self.is_search_failed, queryset = make_filters_products.make_filters()

        return queryset


class FavoritesPage(ListView):
    template_name = "main_favorite/favorites.html"
    model = Products
    context_object_name = 'products'

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()

        if self.request.user.is_authenticated:
            username = self.request.user.username

            filter_favorites = CreateFavoritePage(username, queryset)

            queryset = filter_favorites.create_data_for_favorite_page()

        return queryset


class SaveFavorite(View):
    def post(self, request):
        data = json.loads(self.request.body)

        if self.request.user.is_authenticated:
            save_favorite_object = SaveFavoriteService(data=data)
            save_favorite_object.save_favorite_service()

        return JsonResponse({'message': 'Данные успешно сохранены'})


class BaseInformation(TemplateView):
    template_name = "main_favorite/information.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        information = Information.objects.all()

        context['info'] = information[0]

        return dict(list(context.items()))
