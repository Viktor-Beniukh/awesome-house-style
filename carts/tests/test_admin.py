from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite
from carts.admin import CartTabAdmin, CartAdmin
from carts.models import Cart
from goods.models import Product, Category


class CartAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.cart_admin = CartAdmin(Cart, self.site)
        self.cart_tab_admin = CartTabAdmin(Cart, self.site)
        self.user = get_user_model().objects.create_user(
            email="admin@user.com",
            password="admin12345",
            username="Admin"
        )
        self.category = Category.objects.create(name="Test", slug="test")
        self.product = Product.objects.create(
            name="Product",
            slug="product",
            price=100.0,
            discount=10.0,
            category=self.category
        )
        self.cart = Cart.objects.create(user=self.user, product=self.product, quantity=3)

    def test_user_display_method(self):
        user_display = self.cart_admin.user_display(self.cart)
        self.assertEqual(user_display, str(self.user))

    def test_anonymous_user_display_method(self):
        anonymous_cart = Cart.objects.create(product=self.product, quantity=2)
        user_display = self.cart_admin.user_display(anonymous_cart)
        self.assertEqual(user_display, "Anonym user")

    def test_product_display_method(self):
        product_display = self.cart_admin.product_display(self.cart)
        self.assertEqual(product_display, str(self.product.name))

    def test_cart_tab_admin_fields(self):
        expected_fields = ("product", "quantity", "created_at")
        self.assertEqual(self.cart_tab_admin.fields, expected_fields)

    def test_cart_tab_admin_search_fields(self):
        expected_search_fields = ("product", "quantity", "created_at")
        self.assertEqual(self.cart_tab_admin.search_fields, expected_search_fields)

    def test_cart_tab_admin_readonly_fields(self):
        self.assertEqual(self.cart_tab_admin.readonly_fields, ("created_at",))

    def test_cart_tab_admin_extra(self):
        self.assertEqual(self.cart_tab_admin.extra, 1)

    def test_cart_admin_list_display(self):
        list_display = self.cart_admin.list_display
        expected_list_display = ("user_display", "product_display", "quantity", "created_at",)
        self.assertEqual(list_display, expected_list_display)

    def test_cart_admin_list_filter(self):
        list_filter = self.cart_admin.list_filter
        expected_list_filter = ("created_at", "user", "product__name",)
        self.assertEqual(list_filter, expected_list_filter)
