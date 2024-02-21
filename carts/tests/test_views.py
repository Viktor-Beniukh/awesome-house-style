from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from goods.models import Product, Category
from carts.models import Cart


class CartViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
        )
        self.category = Category.objects.create(name="Test Category", slug="test-category")
        self.product = Product.objects.create(
            name="Product",
            slug="product",
            price=100.0,
            discount=10.0,
            category=self.category
        )
        self.cart = Cart.objects.create(user=self.user, product=self.product, quantity=3)

    def test_cart_add_view_authenticated_user(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("cart:cart_add"), {"product_id": self.product.id}
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()["message"], "Product added to cart")
        self.assertContains(response, "Product added to cart")
        self.assertTemplateUsed(response, "carts/includes/included_cart.html")

    def test_cart_add_view_anonymous_user(self):
        response = self.client.post(
            reverse("cart:cart_add"), {"product_id": self.product.id}
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()["message"], "Product added to cart")
        self.assertContains(response, "Product added to cart")
        self.assertTemplateUsed(response, "carts/includes/included_cart.html")

    def test_cart_change_view(self):
        new_quantity = 5
        response = self.client.post(
            reverse("cart:cart_change"), {"cart_id": self.cart.id, "quantity": new_quantity}
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()["message"], "Quantity changed")
        self.assertEqual(response.json()["quantity"], str(new_quantity))
        self.assertContains(response, "Quantity changed")
        self.assertTemplateUsed(response, "carts/includes/included_cart.html")

    def test_cart_remove_view(self):
        response = self.client.post(reverse("cart:cart_remove"), {"cart_id": self.cart.id})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json()["message"], "Product removed")
        self.assertEqual(response.json()["quantity_deleted"], self.cart.quantity)
        self.assertContains(response, "Product removed")
        self.assertTemplateUsed(response, "carts/includes/included_cart.html")
