from django.db.models import Sum
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .services import (
    AddToPacketProduct,
    ChangeCartQuantity,
    DeleteCartFromPacketLogic,
)
from .utils import (
    get_carts,
    UserOrSessionKeyMixin,
)


class AddProductToPacket(UserOrSessionKeyMixin, View):
    @method_decorator(csrf_exempt)
    def post(self, request):
        product_id = self.request.POST.get("product_id")

        user_or_session_key, is_authenticated = self.get_user_or_created_session_key()

        add_to_packet = AddToPacketProduct(
            is_authenticated,
            product_id,
            user_or_session_key,
        )
        packets = add_to_packet.add_product_packet()

        carts_items_user = render_to_string(
            "modal_packet.html",
            {"packet": packets},
            request=self.request,
        )

        return JsonResponse(
            {
                "message": "packet has updated",
                "carts_items_user": carts_items_user,
            },
        )


class DeleteCartFromPacket(View):
    def post(self, request):
        cart_id = self.request.POST.get("cart_id")
        is_profile = self.request.POST.get("is_profile")

        packet_delete_object = DeleteCartFromPacketLogic(cart_id)
        packet_delete_object.delete_cart_packet()

        packets = get_carts(self.request)
        total_quantity = packets.aggregate(Sum("quantity"))["quantity__sum"] or 0

        if is_profile == "true":
            carts_items_user = render_to_string(
                "users/packet_profile/packet_profile.html",
                {"packet": packets},
                request=self.request,
            )

        else:
            carts_items_user = render_to_string(
                "modal_packet.html",
                {"packet": packets},
                request=self.request,
            )

        return JsonResponse(
            {
                "message": "packet has updated",
                "new_quantity": total_quantity,
                "carts_items_user": carts_items_user,
            },
        )


class ChangeCountProductPacket(UserOrSessionKeyMixin, View):
    @method_decorator(csrf_exempt)
    def post(self, request):
        is_plus = self.request.POST.get("is_plus")
        cart_id = self.request.POST.get("cart_id")
        is_profile = self.request.POST.get("is_profile")

        user_or_session_key, is_authenticated = self.get_user_or_created_session_key()

        packet_object = ChangeCartQuantity(
            is_authenticated,
            user_or_session_key,
            is_plus,
            cart_id,
        )
        packets, new_quantity_packet = packet_object.change_cart_quantity()

        if is_profile == "true":
            carts_items_user = render_to_string(
                "users/packet_profile/packet_profile.html",
                {"packet": packets},
                request=self.request,
            )
        else:
            carts_items_user = render_to_string(
                "modal_packet.html",
                {"packet": packets},
                request=self.request,
            )

        return JsonResponse(
            {
                "message": "packet has updated",
                "new_quantity": new_quantity_packet,
                "carts_items_user": carts_items_user,
            },
        )
