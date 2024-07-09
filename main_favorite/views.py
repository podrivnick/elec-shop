import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_list_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from .models import Information, Products, Categories_Product, Favorites
from django.contrib.auth import get_user_model

from packet.models import Cart
from .utils import q_search

class Main_Page(ListView):
    template_name = "main_favorite/index.html"
    model = Products
    context_object_name = 'products'
    slug_url_kwarg = 'category_slug'
    paginate_by = 6

    def get_context_data(self, *, object_list=None,  **kwargs):
        context = super().get_context_data(**kwargs)

        categories = Categories_Product.objects.all()
        if self.request.user.is_authenticated:
            username = self.request.user.pk

            favorites = Favorites.objects.filter(user=username)
            id_products = [query.product_id for query in favorites]
            context['favorites'] = id_products
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
        self.is_search_failed = False

        if is_available:
            queryset = queryset.filter(count_product__gt=0)
        if is_discount:
            queryset = queryset.filter(discount__gt=0)
        if is_sorting and is_sorting != 'default':
            queryset = queryset.order_by(is_sorting)

        if slug:
            queryset = queryset.filter(category__slug=slug)

        if query:
            queryset = q_search(query, queryset)
            if not len(queryset):
                self.is_search_failed = True

        return queryset


def favorites(request):
    if request.user.is_authenticated:
        username = request.user.username
        user = get_user_model().objects.get(username=username)

        favorites = Favorites.objects.filter(user=user)
        products_id = [item.product_id for item in favorites]

        products = Products.objects.filter(id_product__in=products_id)

        context = {
            "products": products
        }

        return render(request, "main_favorite/favorites.html", context)


def save_favorite(request):

    if request.method == 'POST':
        data = json.loads(request.body)

        username = data['data'][0]
        product_id = data['data'][1]

        try:
            user = get_user_model().objects.get(username=username)
            is_favorite_here = Favorites.objects.get(product_id=product_id, user=user)
            is_favorite_here.delete()
        except Favorites.DoesNotExist:
            new_favorite = Favorites.objects.create(
                product_id=product_id,
                user=user
            )

        return JsonResponse({'message': 'Данные успешно сохранены'})
    else:
        return JsonResponse({'message': 'Неверный метод запроса'}, status=400)


def info(request):
    information = Information.objects.all()

    context = {
        'info': information
    }

    return render(request, "main_favorite/information.html", context)