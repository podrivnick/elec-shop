import json

from django.contrib import messages
from django.http import (
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView

from .forms import FormOpinion
from .models import Opinions
from .services import (
    ChangerCountLikesServices,
    DeleteOpinionServices,
    FinalizeServices,
    GetOpinionsProduct,
    IndexToMove,
    ProductsPageServices,
    SaveOpinionServices,
)
from .utils import GetProductObjectUtils


# from main_favorite.services import CreateFavoritePage
# from core.apps.main.utils import GetUserModel
# from orders.forms import CreateOrder
# from packet.models import Cart


@method_decorator(
    cache_control(no_cache=True, must_revalidate=True, no_store=True),
    name="dispatch",
)
class Product(ListView):
    template_name = "carts_products/cart_product.html"
    model = Products  # noqa
    context_object_name = "products"
    slug_url_kwarg = "product"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        id_product = self.queryset[0].id_product

        get_opinions = GetOpinionsProduct(int(id_product))
        opinions = get_opinions.get_opinions_product()
        count_all_opinions = get_opinions.get_count_opinions()

        context["count_all_opinions"] = count_all_opinions

        if self.request.user.is_authenticated:
            username = self.request.user

            get_product_in_favorite = CreateFavoritePage(username, False)  # noqa
            get_liked_opinion = ProductsPageServices(
                username,
                opinions,
                self.queryset[0],
                True,
            )

            context["favorites"] = (
                get_product_in_favorite.create_data_for_favorite_page()
            )
            opinions, context["liked_objects"] = get_liked_opinion.get_liked_opinions()

        context["opinions"] = opinions[
            0:3
        ]  # выводим только три отзыва на странице продукта
        context["form"] = FormOpinion

        return dict(list(context.items()))

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()

        slug = self.kwargs.get("product")
        if slug:
            queryset = queryset.filter(slug=slug)
            queryset = [item for item in queryset]  # noqa

            self.queryset = queryset

            return queryset[0]

        return queryset


class OpinionsProduct(ListView):
    model = Opinions
    template_name = "carts_products/all_opinions.html"
    context_object_name = "opinions"
    slug_url_kwarg = "product"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        product = GetProductObjectUtils.get_product_object(self.slug)
        context["product"] = product

        if self.request.user.is_authenticated:
            username = self.request.user

            get_liked_opinions = ProductsPageServices(
                username,
                self.queryset,
                product,
                False,
            )

            list_liked_opinion = get_liked_opinions.get_liked_opinions()

            context["liked_objects"] = list_liked_opinion

        return dict(list(context.items()))

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()

        slug = self.kwargs.get("product")
        if slug:
            product = GetProductObjectUtils.get_product_object(str(slug))

            self.slug = str(slug)

            queryset = queryset.filter(id_product=product).select_related("id_product")
            queryset = [item for item in queryset]  # noqa

            self.queryset = queryset

            if self.request.user.is_authenticated:
                get_user_object = GetUserModel(self.request.user)  # noqa
                user = get_user_object.get_user_model()

                index_services = IndexToMove(user, self.queryset)
                self.queryset = index_services.index_to_move_opinions()

        return queryset


@method_decorator(csrf_protect, name="dispatch")
class SaveOpinion(View):
    def post(self, request):
        opinion = self.request.POST.get("message")
        id_product = self.request.POST.get("id_product")
        slug_product = self.request.POST.get("slug_product")

        if self.request.user.is_authenticated:
            username = self.request.user

            save_opinion_at_product = SaveOpinionServices(
                username,
                int(id_product),
                opinion,
            )

            if not save_opinion_at_product.save_opinion_services():
                messages.success(
                    self.request,
                    f"{self.request.user}, u've wrote opinion already",
                )

            return HttpResponseRedirect(
                reverse("carts_products:product", args=[slug_product]),
            )
        else:
            return HttpResponseRedirect(
                reverse("carts_products:product", args=[slug_product]),
            )


class ChangerCountLikeOpinion(View):
    def post(self, request):
        if self.request.user.is_authenticated:
            data = json.loads(self.request.body)

            username = data["data"][0]
            product_id = data["data"][1]
            opinion_id = data["data"][2]

            update_likes = ChangerCountLikesServices(
                username,
                int(product_id),
                int(opinion_id),
            )
            new_count_like = update_likes.change_count_liked_opinions()

            return JsonResponse({"likes_count": new_count_like})
        else:
            return JsonResponse({"message": "Неверный метод запроса"}, status=401)


class DeleteOpinion(View):
    def post(self, request):
        username = self.request.user.username

        slug_product = request.POST.get("product_slug")
        pk_product = request.POST.get("product_pk")

        delete_opinion = DeleteOpinionServices(str(username), int(pk_product))
        delete_opinion.delete_opinion_services()

        return redirect(reverse("carts_products:product", args=[slug_product]))


class Finalize(ListView):
    model = Cart  # noqa
    template_name = "carts_products/finalize_product.html"
    context_object_name = "carts"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        sum_all_carts = sum(cart.products_price() for cart in self.queryset)
        context["total_price"] = sum_all_carts

        username = self.request.user

        object_initial_form = FinalizeServices(username)
        initial_data = object_initial_form.formating_data_of_user_to_form()

        form = CreateOrder(initial=initial_data)  # noqa

        context["form"] = form

        return dict(list(context.items()))  # noqa

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()

        if self.request.user.is_authenticated:
            user = self.request.user

            queryset = queryset.filter(user=user)
            if queryset:
                queryset = [item for item in queryset]  # noqa

            self.queryset = queryset

            return queryset
