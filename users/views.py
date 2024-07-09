from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate
from django.shortcuts import redirect
from django.contrib import messages, auth
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.template.loader import render_to_string


from users.forms import UserLoginForm, UserRegistration, ProfileImages
from .models import *

from packet.models import Cart
from orders.models import Orders, OrderItem
from main_favorite.models import Products

@login_required
def logout_user(request):
    messages.success(request, f"{request.user.username}", 'Вы вышли с аккаунта')
    logout(request)
    return redirect(reverse('main_favorite:index'))

def login(request):
    if request.method == 'POST':
        login_form = UserLoginForm(data=request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']

            user = auth.authenticate(username=username, password=password, email=email)
            session_key = request.session.session_key
            if user:
                auth.login(request, user)
                messages.success(request, f"{username} u've entered to profile")

                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                redirect_page = request.POST.get('next', None)

                if redirect_page and redirect_page != 'user:logout':
                    return HttpResponseRedirect(request.POST.get('next'))

                return HttpResponseRedirect(reverse('main_favorite:index'))

    else:
        login_form = UserLoginForm()

    context = {
        'form': login_form
    }
    return render(request, "users/login.html", context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistration(data=request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(request, username=username, password=password)

            session_key = request.session.session_key

            if user is not None:
                auth.login(request, user)
                messages.success(request, f"{user.username} you've created an account")

                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                return HttpResponseRedirect(reverse('main_favorite:index'))
            else:
                # Обработка случая, если аутентификация не удалась
                messages.error(request, "Failed to authenticate user")

    else:
        form = UserRegistration()

    context = {
        'form': form
    }
    return render(request, "users/registration.html", context)

@login_required
def profile(request):
    context = {
        'is_packet': True
    }

    if request.method == 'POST':
        form = ProfileImages(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            if request.user:
                user.username = request.user.username
                user.save(update_fields=['username'])
            if request.FILES.get('avatar'):
                user.image = request.FILES['avatar']
                user.save(update_fields=['image'])

            messages.success(request, f"{request.user} u've update profile")
            return HttpResponseRedirect(reverse("users:profile"))
    else:
        form = ProfileImages(instance=request.user)
        if request.GET.dict():
            user = form.save(commit=False)
            all_new_data = request.GET.dict()
            for par, value in all_new_data.items():
                if not value:
                    continue
                setattr(user, par, value)
                user.save(update_fields=[par])
            messages.success(request, f"u've update profile,\n new data will be reflection after clearing cash")

        user = get_user_model().objects.get(username=request.user)

        carts = Cart.objects.filter(user=user)
        list_carts = [cart for cart in carts]

        context['packet'] = list_carts

    context['form'] = form

    return render(request, "users/profile.html", context)

def change_below_profile(request):
    if request.method == 'POST':
        is_packet = request.POST.get('is_packet')

        if is_packet == 'order':
            carts_items_user = render_to_string(
                "users/packet_profile/orders_profile.html", {"is_packet": False}, request=request)
        else:
            carts_items_user = render_to_string(
            "users/packet_profile/packet_profile.html", {"is_packet": True}, request=request)

        return JsonResponse({
            'message': 'packet has updated',
            'carts_items_user': carts_items_user
        })
    else:
        return JsonResponse({'message': 'Неверный метод запроса'}, status=400)

