from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View

from .services import AddToPacketProduct, DeleteCartFromPacketLogic, ChangeCartQuantity
from .utils import get_carts


class AddProductToPacket(View):
    def post(self, request):

        product_id = self.request.POST.get("product_id")

        if self.request.user.is_authenticated:
            username = self.request.user.username
            user = get_user_model().objects.get(username=username)

            add_to_packet = AddToPacketProduct(True, product_id, user)
            add_to_packet.add_product_packet()
        else:
            add_to_packet = AddToPacketProduct(False, product_id, self.request.session.session_key)
            add_to_packet.add_product_packet()

        packets = get_carts(self.request)
        carts_items_user = render_to_string(
            "modal_packet.html",
            {"packet": packets},
            request=self.request
        )

        return JsonResponse({
            'message': 'packet has updated',
            'carts_items_user': carts_items_user
        })


class DeleteCartFromPacket(View):

    def post(self, request):
        cart_id = self.request.POST.get('cart_id')
        is_profile = self.request.POST.get('is_profile')

        if self.request.user.is_authenticated:
            user = get_user_model().objects.get(username=self.request.user)
            packet_delete_object = DeleteCartFromPacketLogic(True, cart_id, user)
        else:
            session_key = self.request.session.session_key
            packet_delete_object = DeleteCartFromPacketLogic(False, cart_id, session_key)

        new_quantity = packet_delete_object.delete_cart_packet()

        packets = get_carts(self.request)

        if is_profile == 'true':
            carts_items_user = render_to_string(
                "users/packet_profile/packet_profile.html",
                {"packet": packets},
                request=self.request
            )

        else:
            carts_items_user = render_to_string(
                "modal_packet.html",
                {"packet": packets},
                request=self.request
            )

        return JsonResponse({
            'message': 'packet has updated',
            'new_quantity': new_quantity,
            'carts_items_user': carts_items_user
        })


class ChangeCountProductPacket(View):
    def post(self, request):
        is_plus = self.request.POST.get('is_plus')
        cart_id = self.request.POST.get('cart_id')
        is_profile = self.request.POST.get('is_profile')

        if self.request.user.is_authenticated:
            user = get_user_model().objects.get(username=self.request.user)
            packet_change_quantity = ChangeCartQuantity(True, is_plus, cart_id, user)
        else:
            session_key = self.request.session.session_key
            packet_change_quantity = ChangeCartQuantity(False, is_plus, cart_id, session_key)

        new_quantity = packet_change_quantity.change_cart_quantity()

        packets = get_carts(self.request)

        if is_profile == 'true':
            carts_items_user = render_to_string(
                "users/packet_profile/packet_profile.html",
                {"packet": packets},
                request=self.request
            )
        else:
            carts_items_user = render_to_string(
            "modal_packet.html",
            {"packet": packets},
            request=self.request)

        return JsonResponse({
            'message': 'packet has updated',
            'new_quantity': new_quantity,
            'carts_items_user': carts_items_user
        })
















