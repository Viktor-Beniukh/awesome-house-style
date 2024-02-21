from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from goods.models import Product, Category, FavoriteProduct

User = get_user_model()


FAVORITE_PRODUCT_URL = reverse("catalog:favorite_products")
TOGGLE_FAVORITE_URL = reverse("catalog:toggle_favorite")


class PublicFavoriteProductsViewTests(TestCase):

    def test_login_required(self):

        response = self.client.get(FAVORITE_PRODUCT_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateFavoriteProductsViewTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
        )
        self.client.force_login(self.user)

        self.category = Category.objects.create(name="Test Category", slug="test-category")

    def test_favorite_products_view(self):
        product1 = Product.objects.create(name="Product 1", price=10.0, category=self.category)
        product2 = Product.objects.create(name="Product 2", price=15.0, category=self.category)

        FavoriteProduct.objects.create(user=self.user, product=product1)
        FavoriteProduct.objects.create(user=self.user, product=product2)

        response = self.client.get(FAVORITE_PRODUCT_URL)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "goods/favorite_products.html")

        self.assertContains(response, "Product 1")
        self.assertContains(response, "Product 2")


class PublicToggleFavoriteViewTests(TestCase):

    def test_login_required(self):

        response = self.client.get(TOGGLE_FAVORITE_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateToggleFavoriteViewTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
        )
        self.client.force_login(self.user)

        self.category = Category.objects.create(name="Test Category", slug="test-category")

        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=50.25,
            discount=2.0,
            quantity=2,
            category=self.category
        )

        self.url = TOGGLE_FAVORITE_URL

    def test_toggle_favorite_view_toggle_on(self):
        response = self.client.post(self.url, {"product_id": self.product.id})

        self.assertEqual(response.status_code, 200)

        json_response = response.json()
        self.assertTrue(json_response["is_favorite"])
        self.assertEqual(json_response["favorites_count"], 1)

    def test_toggle_favorite_view_toggle_off(self):
        response_toggle_on = self.client.post(self.url, {"product_id": self.product.id})

        self.assertEqual(response_toggle_on.status_code, 200)

        json_response_toggle_on = response_toggle_on.json()
        self.assertTrue(json_response_toggle_on["is_favorite"])
        self.assertEqual(json_response_toggle_on["favorites_count"], 1)

        response_toggle_off = self.client.post(self.url, {"product_id": self.product.id})

        self.assertEqual(response_toggle_off.status_code, 200)

        json_response_toggle_off = response_toggle_off.json()
        self.assertFalse(json_response_toggle_off["is_favorite"])
        self.assertEqual(json_response_toggle_off["favorites_count"], 0)

    def test_toggle_favorite_view_invalid_product_id(self):
        response = self.client.post(self.url, {"product_id": "invalid_id"})

        self.assertEqual(response.status_code, 400)

        json_response = response.json()
        self.assertIn("error", json_response)
        self.assertEqual(json_response["error"], "Invalid product_id")

    def test_toggle_favorite_view_invalid_method(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)

        json_response = response.json()
        self.assertIn("error", json_response)
        self.assertEqual(json_response["error"], "Method not allowed")
