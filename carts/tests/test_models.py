from django.test import TestCase
from django.contrib.auth import get_user_model
from goods.models import Product, Category
from carts.models import Cart


class CartModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
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

    def test_cart_str_method(self):
        cart = Cart(user=self.user, product=self.product, quantity=3)
        self.assertEqual(
            str(cart),
            f"Cart {self.user.username} | Product {self.product.name} | Quantity 3"
        )

    def test_anonymous_cart_str_method(self):
        cart = Cart(product=self.product, quantity=2)
        self.assertEqual(
            str(cart),
            f"Anonym cart | Product {self.product.name} | Quantity 2"
        )

    def test_products_price_method(self):
        cart = Cart(user=self.user, product=self.product, quantity=5)
        expected_price = round(self.product.sell_price() * 5, 2)
        self.assertEqual(cart.products_price(), expected_price)

    def test_total_price_method(self):
        Cart.objects.create(user=self.user, product=self.product, quantity=3)
        another_product = Product.objects.create(
            name="Another Test Product",
            price=50.0,
            discount=10.0,
            category=self.category
        )
        Cart.objects.create(user=self.user, product=another_product, quantity=2)

        total_price = Cart.objects.total_price()
        expected_total_price = (
            self.product.sell_price() * 3 + another_product.sell_price() * 2
        )

        self.assertEqual(total_price, expected_total_price)

    def test_total_quantity_method(self):
        Cart.objects.create(user=self.user, product=self.product, quantity=3)
        another_product = Product.objects.create(
            name="Another Test Product",
            price=70.0,
            discount=5.0,
            category=self.category
        )
        Cart.objects.create(user=self.user, product=another_product, quantity=2)

        total_quantity = Cart.objects.total_quantity()
        expected_total_quantity = 3 + 2

        self.assertEqual(total_quantity, expected_total_quantity)
