from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from .utils import get_carts
from .models import Cart
from main_favorite.models import Products


def save_packet(request):
    if request.method == 'POST':
        product_id = request.POST.get("product_id")
        product = Products.objects.get(id_product=product_id)

        if request.user.is_authenticated:
            username = request.user.username
            user = get_user_model().objects.get(username=username)

            packet = Cart.objects.filter(user=user, product=product)

            if packet:
                packet = [item_packet for item_packet in packet]
                packet[0].quantity = packet[0].quantity + 1

                packet[0].save()
            else:
                packet = Cart.objects.create(
                    user=user,
                    product=product,
                    quantity=1,
                )
        else:
            packet = Cart.objects.filter(session_key=request.session.session_key, product=product)

            if packet:
                packet = [item_packet for item_packet in packet]
                packet[0].quantity = packet[0].quantity + 1

                packet[0].save()
            else:
                packet = Cart.objects.create(
                    session_key=request.session.session_key,
                    product=product,
                    quantity=1,
                )

        packets = get_carts(request)
        carts_items_user = render_to_string(
        "modal_packet.html", {"packet": packets}, request=request)

        return JsonResponse({
            'message': 'packet has updated',
            'carts_items_user': carts_items_user
        })
    else:
        return JsonResponse({'message': 'Неверный метод запроса'}, status=400)


def delete_cart(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        is_profile = request.POST.get('is_profile')
        cart = Cart.objects.get(pk=cart_id)
        cart.delete()

        user = get_user_model().objects.get(username=request.user)

        carts_left = Cart.objects.filter(user=user)
        new_quantity = sum([item.quantity for item in carts_left])

        packets = get_carts(request)
        if is_profile == 'true':
            carts_items_user = render_to_string(
                "users/packet_profile/packet_profile.html", {"packet": packets}, request=request)
        else:
            carts_items_user = render_to_string(
            "modal_packet.html", {"packet": packets}, request=request)

        return JsonResponse({
            'message': 'packet has updated',
            'new_quantity': new_quantity,
            'carts_items_user': carts_items_user
        })
    else:
        return JsonResponse({'message': 'Неверный метод запроса'}, status=400)

def change_count_product(request):
    if request.method == 'POST':
        is_plus = request.POST.get('is_plus')
        cart_id = request.POST.get('cart_id')
        is_profile = request.POST.get('is_profile')

        cart = Cart.objects.get(pk=cart_id)

        if is_plus == 'true':
            cart.quantity = cart.quantity + 1
            cart.save()
        elif is_plus == 'false':
            cart.quantity = cart.quantity - 1
            if cart.quantity == 0:
                cart.delete()
            else:
                cart.save()

        user = get_user_model().objects.get(username=request.user)

        carts = Cart.objects.filter(user=user)

        new_quantity = sum([item.quantity for item in carts])

        packets = get_carts(request)

        if is_profile == 'true':
            carts_items_user = render_to_string(
                "users/packet_profile/packet_profile.html", {"packet": packets}, request=request)
        else:
            carts_items_user = render_to_string(
            "modal_packet.html", {"packet": packets}, request=request)

        return JsonResponse({
            'message': 'packet has updated',
            'new_quantity': new_quantity,
            'carts_items_user': carts_items_user
        })
    else:
        return JsonResponse({'message': 'Неверный метод запроса'}, status=400)















