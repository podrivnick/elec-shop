from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class userAdministration(UserAdmin):
    search_fields = ["username", "email", "phone"]
    list_filter = ["is_active", "is_superuser"]
    list_display = [
        "username",
        "email",
        "phone",
        "is_active",
        "is_superuser",
        "date_joined",
    ]
    ordering = ["-date_joined"]
    readonly_fields = ["last_login", "date_joined"]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal Info",
            {"fields": ("first_name", "last_name", "email", "phone", "age", "image")},
        ),
        (
            "Permissions",
            {"fields": ("is_active", "is_superuser", "groups", "user_permissions")},
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
