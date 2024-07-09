import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import ListView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages, auth
from datetime import date
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control

from orders.forms import CreateOrder
from packet.models import Cart
from main_favorite.models import Products, Favorites
from .models import Opinions, LikesOpinion
from .forms import FormOpinion

data_form_finalize = {
    'first_name': 'first_name',
    'last_name': 'last_name',
    'email': 'email',
    'phone': 'phone',
}

@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='dispatch')
class Product(ListView):
    template_name = "carts_products/cart_product.html"
    model = Products
    context_object_name = 'products'
    slug_url_kwarg = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        id_product = self.queryset[0].id_product

        opinions = Opinions.objects.filter(id_product=id_product).select_related('id_product', 'user')
        opinions = [item for item in opinions]
        count_all_opinions = len(opinions)
        context['count_all_opinions'] = count_all_opinions

        if self.request.user.is_authenticated:
            username = self.request.user

            favorites = Favorites.objects.filter(user=username)
            id_products = [query.product_id for query in favorites]

            context['favorites'] = id_products

            user = get_user_model().objects.get(username=self.request.user)
            product_object = Products.objects.get(id_product=id_product)
            list_liked_opinion = []

            for object_opinion in opinions:
                is_liked_opinion = LikesOpinion.objects.filter(user=user, id_product=product_object, opinion_id=object_opinion.pk).select_related("id_product", 'user')
                list_liked_opinion.append(is_liked_opinion.first())

            context['liked_objects'] = list_liked_opinion

            index_to_move = next((i for i, item in enumerate(opinions) if item.user == user), None)

            if index_to_move is not None:
                opinions.insert(0, opinions.pop(index_to_move))

        context['opinions'] = opinions[0:3]
        context['form'] = FormOpinion

        return dict(list(context.items()))

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()

        slug = self.kwargs.get('product')
        if slug:
            queryset = queryset.filter(slug=slug)
            queryset = [item for item in queryset]
            self.queryset = queryset
            return queryset[0]

        return queryset

class OpinionsProduct(ListView):
    model = Opinions
    template_name = "carts_products/all_opinions.html"
    context_object_name = 'opinions'
    slug_url_kwarg = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        product = Products.objects.get(slug=self.slug)
        context['product'] = product

        list_liked_opinion = []
        if self.request.user.is_authenticated:
            username = self.request.user
            user = get_user_model().objects.get(username=username)

            for object_opinion in self.queryset:
                is_liked_opinion = LikesOpinion.objects.filter(user=user, id_product=product,
                                                               opinion_id=object_opinion.pk).select_related('id_product')
                list_liked_opinion.append(is_liked_opinion.first())

            context['liked_objects'] = list_liked_opinion

        return dict(list(context.items()))

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()

        slug = self.kwargs.get('product')
        if slug:
            product = Products.objects.get(slug=slug)
            self.slug = slug

            queryset = queryset.filter(id_product=product).select_related('id_product')
            queryset = [item for item in queryset]
            self.queryset = queryset

            if self.request.user.is_authenticated:
                user = get_user_model().objects.get(username=self.request.user)

                index_to_move = next((i for i, item in enumerate(self.queryset) if item.user == user), None)

                if index_to_move is not None:
                    self.queryset.insert(0, self.queryset.pop(index_to_move))

        return queryset


@csrf_protect
def save_opinion(request):
    if request.method == 'POST':
        form = FormOpinion(data=request.POST)
        if form.is_valid():
            opinion = request.POST.get('message')
            id_product = request.POST.get('id_product')
            slug_product = request.POST.get('slug_product')

            if request.user.is_authenticated:
                user = get_user_model().objects.get(username=request.user.username)
                opinions = Opinions.objects.filter(id_product=id_product, user=user)

                product = Products.objects.get(id_product=id_product)
                if opinions:
                    messages.success(request, f"{request.user}, u've wrote opinion already")
                else:
                    opinions = Opinions.objects.create(
                        id_product=product,
                        opinion=opinion,
                        user=user,
                        data_added=date.today()
                    )
                return HttpResponseRedirect(reverse("carts_products:product", args=[slug_product]))
    else:
        return render(request, 'main_favorite/index.html')

def save_like_opinion(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        username = data['data'][0]
        product_id = data['data'][1]
        opinion_id = data['data'][2]

        user = get_user_model().objects.get(username=username)
        product = Products.objects.get(id_product=product_id)
        opinion = Opinions.objects.get(pk=opinion_id, id_product=product)

        try:
            is_opinion_liked = LikesOpinion.objects.get(user=user, id_product=product, opinion_id=opinion)
            is_opinion_liked.delete()
            opinion.likes = opinion.likes - 1
            new_count_like = opinion.likes

            opinion.save()
        except LikesOpinion.DoesNotExist:
            is_opinion_liked = LikesOpinion.objects.create(
                user=user,
                id_product=product,
                opinion_id=opinion
            )
            opinion.likes = opinion.likes + 1
            new_count_like = opinion.likes
            opinion.save()
        return JsonResponse({'likes_count': new_count_like})
    else:
        return JsonResponse({'message': 'Неверный метод запроса'}, status=400)


def delete_opinion(request):
    if request.method == 'POST':
        user = get_user_model().objects.get(username=request.user.username)

        slug_product = request.POST.get('product_slug')
        pk_product = request.POST.get('product_pk')
        opinion_user = Opinions.objects.get(user=user, id_product=pk_product)
        opinion_user.delete()

        return redirect(reverse('carts_products:product', args=[slug_product]))
    else:
        return JsonResponse({'message': 'Неверный метод запроса'}, status=400)

def finalize_product(request):
    return render(request, "carts_products/finalize_product.html")

class Finalize(ListView):
    model = Cart
    template_name = "carts_products/finalize_product.html"
    context_object_name = 'carts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        sum_all_carts = sum([cart.products_price() for cart in self.queryset])
        context['total_price'] = sum_all_carts

        user = get_user_model().objects.get(username=self.request.user)

        initial_data = {}
        for key, value in data_form_finalize.items():
            try:
                initial_data[key] = getattr(user, value)
            except user.DoesNotExist:
                pass

        form = CreateOrder(initial=initial_data)

        context['form'] = form

        return dict(list(context.items()))

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()

        if self.request.user.is_authenticated:
            user = self.request.user

            queryset = queryset.filter(user=user)
            if queryset:
                queryset = [item for item in queryset]
            self.queryset = queryset
            return queryset