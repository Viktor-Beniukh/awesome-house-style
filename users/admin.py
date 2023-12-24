from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("phone_number", "image_user")
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("phone_number", "image_user")}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "image_user",
                        "phone_number",
                    )
                },
            ),
        )
    )
