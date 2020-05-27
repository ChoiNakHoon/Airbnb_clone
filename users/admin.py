from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from rooms.models import Room


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """ Custom User Admin """

    CUSTOM_PROFILE_FILED = (
        (
            "Custom Profile",
            {
                "fields": (
                    "superhost",
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "login_method",
                )
            },
        ),
    )

    fieldsets = UserAdmin.fieldsets + CUSTOM_PROFILE_FILED

    list_display = UserAdmin.list_display + (
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_superuser",
        "email_verified",
        "email_secret",
        "login_method",
    )

    list_filter = UserAdmin.list_filter + ("superhost",)
