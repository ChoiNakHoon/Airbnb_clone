from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.
@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """ Custom User Admin """

    CUSTOM_PROFILE_FILED = (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
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
    )

    list_filter = UserAdmin.list_filter + ("superhost",)
