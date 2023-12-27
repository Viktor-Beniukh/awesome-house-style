from django.contrib import admin

from carts.models import Cart


class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = "product", "quantity", "created_at"
    search_fields = "product", "quantity", "created_at"
    readonly_fields = ("created_at",)
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user_display", "product_display", "quantity", "created_at",)
    list_filter = ("created_at", "user", "product__name",)

    @staticmethod
    def user_display(obj):
        if obj.user:
            return str(obj.user)
        return "Anonym user"

    @staticmethod
    def product_display(obj):
        return str(obj.product.name)
