from django.contrib import messages
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import (
    redirect,
    render,
)
from django.urls import reverse

from core.api.schemas import (
    SuccessResponse,
    Template,
)
from core.api.v1.users.dto.base import DTOProifleAPI
from core.api.v1.users.dto.responses import (
    DTOResponseAuthenticateAPI,
    DTOResponseLoginAPI,
    DTOResponseLogoutPageAPI,
    DTOResponseProfileAPI,
    DTOResponseRegisterAPI,
    DTOResponseRegistrationAPI,
)
from core.apps.users.config.config import (
    MESSAGE_UPDATE_PROFILE,
    MESSAGE_UPDATED_AVATAR_OR_USERNAME,
)


def render_login(
    request: HttpRequest,
    response: SuccessResponse[DTOResponseLoginAPI],
    template: Template,
) -> HttpResponse:
    """Возвращает либо JSON-ответ, либо HTML в зависимости от типа запроса."""
    if request.headers.get("Content-Type") == "application/json":
        return JsonResponse(
            {
                "status": response.status,
                "result": {
                    "form": response.result,
                },
            },
        )
    else:
        return render(
            request,
            template,
            {
                "form": response.result,
            },
        )


def render_authenticate(
    request: HttpRequest,
    response: SuccessResponse[DTOResponseAuthenticateAPI],
    template: Template,
) -> HttpResponse:
    """Возвращает либо JSON-ответ, либо HTML в зависимости от типа запроса."""
    if request.headers.get("Content-Type") == "application/json":
        return JsonResponse(
            {
                "status": response.status,
                "result": {
                    "username": response.result.username,
                },
            },
        )
    else:
        messages.success(request, f"{response.result.username} u've entered to profile")

        return HttpResponseRedirect(reverse("v1:index", args=["all"]))


def render_logout(
    request: HttpRequest,
    response: SuccessResponse[DTOResponseLogoutPageAPI],
    template: Template,
) -> HttpResponse:
    """Возвращает либо JSON-ответ, либо HTML в зависимости от типа запроса."""
    if request.headers.get("Content-Type") == "application/json":
        return JsonResponse(
            {
                "status": response.status,
                "result": {
                    "username": response.result.username,
                },
            },
        )
    else:
        messages.success(
            request,
            f"{response.result.username} u've logouted from profile",
        )

        return HttpResponseRedirect(reverse("v1:index", args=["all"]))


def render_registration(
    request: HttpRequest,
    response: SuccessResponse[DTOResponseRegistrationAPI],
    template: Template,
) -> HttpResponse:
    """Возвращает либо JSON-ответ, либо HTML в зависимости от типа запроса."""
    if request.headers.get("Content-Type") == "application/json":
        return JsonResponse(
            {
                "status": response.status,
                "result": {
                    "form": response.result,
                },
            },
        )
    else:
        return render(
            request,
            template,
            {
                "form": response.result,
            },
        )


def render_register(
    request: HttpRequest,
    response: SuccessResponse[DTOResponseRegisterAPI],
    template: Template,
) -> HttpResponse:
    """Возвращает либо JSON-ответ, либо HTML в зависимости от типа запроса."""
    if request.headers.get("Content-Type") == "application/json":
        return JsonResponse(
            {
                "status": response.status,
                "result": {
                    "username": response.result.username,
                },
            },
        )
    else:
        messages.success(request, f"{response.result.username} u've created profile")

        return HttpResponseRedirect(reverse("v1:index", args=["all"]))


def render_profile_page(
    request: HttpRequest,
    response: SuccessResponse[DTOResponseProfileAPI],
    template: Template,
) -> HttpResponse:
    """Возвращает либо JSON-ответ, либо HTML в зависимости от типа запроса."""
    if request.headers.get("Content-Type") == "application/json":
        return JsonResponse(
            {
                "status": response.status,
                "result": {
                    "form": response.result.form,
                    "is_packet": response.result.is_packet,
                    "packet": response.result.packet,
                },
            },
        )
    else:
        if response.result.referer is not None:
            messages.success(request, MESSAGE_UPDATE_PROFILE)
            return redirect(response.result.referer)
        return render(
            request,
            template,
            {
                "form": response.result.form,
                "is_packet": response.result.is_packet,
                "packet": response.result.packet,
            },
        )


def render_profile(
    request: HttpRequest,
    response: SuccessResponse[DTOProifleAPI],
    template: Template,
) -> HttpResponse:
    """Возвращает либо JSON-ответ, либо HTML в зависимости от типа запроса."""
    if request.headers.get("Content-Type") == "application/json":
        return JsonResponse(
            {
                "status": response.status,
                "result": {},
            },
        )
    else:
        if response.result.referer is not None:
            messages.success(request, MESSAGE_UPDATED_AVATAR_OR_USERNAME)
            return redirect(response.result.referer)

        return render(
            request,
            template,
            {},
        )
