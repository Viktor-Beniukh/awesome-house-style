from django.contrib import admin
from django.utils.safestring import mark_safe

from goods.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "image_show",
        "price",
        "quantity",
        "created_at",
        "updated_at"
    )
    list_filter = ("created_at", "updated_at")
    list_editable = ("price",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)

    def image_show(self, obj):
        if obj.image_product:
            return mark_safe(
                "<img src='{}' width='60' />".format(obj.image_product.url)
            )
        return "None"

    image_show.__name__ = "Picture"
