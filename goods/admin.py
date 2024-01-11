from django.contrib import admin
from django.utils.safestring import mark_safe

from goods.models import Category, Product, Review, FavoriteProduct, Rating


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "discount",
        "quantity",
        "created_at",
        "updated_at",
        "image_show",
    )
    list_filter = ("discount", "category")
    list_editable = ("price", "discount", "quantity")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    fields = (
        "name",
        "category",
        "slug",
        "description",
        "image_product",
        ("price", "discount"),
        "quantity"
    )

    def image_show(self, obj):
        if obj.image_product:
            return mark_safe(
                "<img src='{}' width='50' />".format(obj.image_product.url)
            )
        return "None"

    image_show.__name__ = "Picture"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "parent", "product")
    readonly_fields = ("user",)


@admin.register(FavoriteProduct)
class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ("product", "user")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("product", "rating", "user")
