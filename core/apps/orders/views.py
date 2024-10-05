from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from core.apps.main.utils.main import GetUserModel

from .config import SUCCESSFUL_ORDER
from .exceptions import BaseOrderException
from .models import Orders
from .services import CreateBasicOrders


class CreateNewOrder(LoginRequiredMixin, View):
    template_name = "carts_products/finalize_product.html"

    def post(self, request):
        username = self.request.user

        user_model = GetUserModel(username)
        user = user_model.get_user_model()

        first_name = self.request.POST.get("first_name")
        last_name = self.request.POST.get("last_name")
        email = self.request.POST.get("email")
        phone = self.request.POST.get("phone")
        delivery_address = self.request.POST.get("delivery_address")
        required_delivery = self.request.POST.get("required_delivery")
        payment_on_get = self.request.POST.get("payment_on_get")
        total_price = self.request.POST.get("total_price")

        basic_orders = Orders.objects.create(
            user=user,
            name_receiver=first_name,
            surname_receiver=last_name,
            phone_number=phone,
            required_delivery=required_delivery,
            delivery_address=delivery_address,
            has_paid=False,
            email=email,
            payment_on_get=payment_on_get,
            total_price=total_price,
        )

        try:
            order = CreateBasicOrders(
                user,
                basic_orders,
            )
            order.create_order()

        except BaseOrderException as error:
            basic_orders.delete()
            messages.success(request, f"{error.exception}")

            return redirect(reverse("carts_products:finalize_product"))

        else:
            messages.success(request, SUCCESSFUL_ORDER)

            return redirect(reverse("main_favorite:index"))
