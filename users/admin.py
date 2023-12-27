from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from carts.admin import CartTabAdmin
from users.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("phone_number", "image_show")
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("phone_number", "image_user")}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "email",
                        "phone_number",
                        "image_user",
                    )
                },
            ),
        )
    )

    inlines = [CartTabAdmin, ]

    def image_show(self, obj):
        if obj.image_user:
            return mark_safe(
                "<img src='{}' width='30' />".format(obj.image_user.url)
            )
        return "None"

    image_show.__name__ = "Picture"
