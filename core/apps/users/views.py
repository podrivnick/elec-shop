from django.contrib import (
    auth,
    messages,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from django.http import (
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import (
    reverse,
    reverse_lazy,
)
from django.views import View
from django.views.generic import (
    CreateView,
    TemplateView,
)

from main_favorite.utils import GetUserModel
from packet.models import Cart

from .config import (
    MESSAGE_LOGOUT,
    MESSAGE_UPDATE_PROFILE,
    MESSAGE_UPDATED_AVATAR_OR_USERNAME,
)
from .forms import (
    ProfileImages,
    UserLoginForm,
    UserRegistration,
)
from .services import (
    AddSessionCartToUser,
    ChangeProfileUserData,
    UpdateProfileAvatarUsername,
)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("main_favorite:index")

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, f"{MESSAGE_LOGOUT} {request.user.username}")
        return super().dispatch(request, *args, **kwargs)


class LoginUser(LoginView):
    form_class = UserLoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy("main_favorite:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = UserLoginForm()

        return context

    def form_valid(self, form):
        user = form.get_user()
        session_key = self.request.session.session_key or False

        if user:
            auth.login(self.request, user)

            username = form.cleaned_data["username"]
            messages.success(self.request, f"{username} u've entered to profile")

            add_session_packet_to_user = AddSessionCartToUser(session_key, user)
            add_session_packet_to_user.add_session_cart_to_user()

            return HttpResponseRedirect(reverse("main_favorite:index"))


class RegisterUser(CreateView):
    form_class = UserRegistration
    template_name = "users/registration.html"
    success_url = reverse_lazy("main_favorite:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = UserRegistration()

        return context

    def form_valid(self, form):
        session_key = self.request.session.session_key or False
        user = form.instance

        if user:
            form.save()
            auth.login(self.request, user)

            add_session_packet_to_user = AddSessionCartToUser(session_key, user)
            add_session_packet_to_user.add_session_cart_to_user()

            messages.success(self.request, f"{user.username} you've created an account")

            return HttpResponseRedirect(reverse("main_favorite:index"))


class ProfileUserData(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = GetUserModel(self.request.user).get_user_model()

        carts = Cart.objects.filter(user=user).order_by("-quantity")
        list_carts = [cart for cart in carts]  # noqa

        context["form"] = ProfileImages(instance=self.request.user)
        context["is_packet"] = True
        context["packet"] = list_carts

        return context

    def get(self, request, *args, **kwargs):
        if self.request.GET.dict():
            form = ProfileImages(instance=self.request.user)
            user_data = form.save(commit=False)
            all_new_data = self.request.GET.dict()

            change_profile = ChangeProfileUserData(user_data, all_new_data)
            change_profile.change_profile()

            messages.success(self.request, MESSAGE_UPDATE_PROFILE)

            # Перенаправляем на страницу, с которой пришел запрос
            referer = request.META.get("HTTP_REFERER")
            if referer:
                return redirect(referer)
            else:
                return redirect(self.success_url)
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request):
        form = ProfileImages(
            data=self.request.POST,
            instance=self.request.user,
            files=self.request.FILES,
        )

        if form.is_valid():
            user = form.save(commit=False)

            change_user_avatar_or_username = UpdateProfileAvatarUsername(
                user,
                self.request.POST,
                self.request.FILES,
            )
            change_user_avatar_or_username.change_avatar_or_username()

            messages.success(
                self.request,
                f"{MESSAGE_UPDATED_AVATAR_OR_USERNAME}{self.request.user}",
            )

            return redirect("users:profile")

        return self.render_to_response(self.get_context_data(form=form))


class ChangeDataBelowProfile(View):
    def post(self, request):
        is_packet = self.request.POST.get("is_packet")

        if is_packet == "order":
            carts_items_user = render_to_string(
                "users/packet_profile/orders_profile.html",
                {"is_packet": False},
                request=self.request,
            )
        else:
            carts_items_user = render_to_string(
                "users/packet_profile/packet_profile.html",
                {"is_packet": True},
                request=self.request,
            )

        return JsonResponse(
            {
                "message": "packet has updated",
                "carts_items_user": carts_items_user,
            },
        )
