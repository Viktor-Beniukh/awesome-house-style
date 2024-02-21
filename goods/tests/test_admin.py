from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from goods.admin import (
    CategoryAdmin, ProductAdmin, ReviewAdmin, FavoriteProductAdmin, RatingAdmin
)
from goods.models import Category, Product, Review, FavoriteProduct, Rating


class CategoryAdminTest(TestCase):
    def setUp(self):
        self.admin_site = AdminSite()
        self.category_admin = CategoryAdmin(Category, self.admin_site)

    def test_list_display(self):
        self.assertEqual(self.category_admin.list_display, ("name", "slug"))

    def test_prepopulated_fields(self):
        self.assertEqual(self.category_admin.prepopulated_fields, {"slug": ("name",)})

    def test_search_fields(self):
        self.assertEqual(self.category_admin.search_fields, ("name",))


class ProductAdminTest(TestCase):
    def setUp(self):
        self.admin_site = AdminSite()
        self.product_admin = ProductAdmin(Product, self.admin_site)

    def test_list_display(self):
        expected_list_display = (
            "name",
            "price",
            "discount",
            "quantity",
            "created_at",
            "updated_at",
            "image_show",
        )
        self.assertEqual(self.product_admin.list_display, expected_list_display)

    def test_list_filter(self):
        expected_list_filter = ("discount", "category")
        self.assertEqual(self.product_admin.list_filter, expected_list_filter)

    def test_list_editable(self):
        expected_list_editable = ("price", "discount", "quantity")
        self.assertEqual(self.product_admin.list_editable, expected_list_editable)

    def test_prepopulated_fields(self):
        self.assertEqual(self.product_admin.prepopulated_fields, {"slug": ("name",)})

    def test_search_fields(self):
        self.assertEqual(self.product_admin.search_fields, ("name",))

    def test_fields(self):
        expected_fields = (
            "name",
            "category",
            "slug",
            "description",
            "image_product",
            ("price", "discount"),
            "quantity",
        )
        self.assertEqual(self.product_admin.fields, expected_fields)


class ReviewAdminTest(TestCase):
    def setUp(self):
        self.admin_site = AdminSite()
        self.review_admin = ReviewAdmin(Review, self.admin_site)

    def test_list_display(self):
        expected_list_display = ("user", "parent", "product")
        self.assertEqual(self.review_admin.list_display, expected_list_display)

    def test_readonly_fields(self):
        expected_readonly_fields = ("user",)
        self.assertEqual(self.review_admin.readonly_fields, expected_readonly_fields)


class FavoriteProductAdminTest(TestCase):
    def setUp(self):
        self.admin_site = AdminSite()
        self.review_admin = FavoriteProductAdmin(FavoriteProduct, self.admin_site)

    def test_list_display(self):
        expected_list_display = ("product", "user")
        self.assertEqual(self.review_admin.list_display, expected_list_display)


class RatingAdminTest(TestCase):
    def setUp(self):
        self.admin_site = AdminSite()
        self.review_admin = RatingAdmin(Rating, self.admin_site)

    def test_list_display(self):
        expected_list_display = ("product", "rating", "user")
        self.assertEqual(self.review_admin.list_display, expected_list_display)
