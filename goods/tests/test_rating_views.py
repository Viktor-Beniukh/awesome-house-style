from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from goods.models import Product, Category

User = get_user_model()


def detail_rating_url(product_id: int):
    return reverse("catalog:add_rating", args=[product_id])


class PublicAddRatingViewTests(TestCase):

    def setUp(self) -> None:
        self.category = Category.objects.create(name="Test", slug="test")

        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=50.25,
            discount=2.0,
            quantity=2,
            category=self.category
        )

    def test_login_required(self):
        rating_url = detail_rating_url(self.product.id)
        response = self.client.get(rating_url)

        self.assertNotEqual(response.status_code, 200)


class PrivateAddRatingViewTest(TestCase):

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

        self.url = detail_rating_url(self.product.id)

    def test_add_rating_view_success(self):

        response = self.client.post(self.url, {"rating": 4})

        self.assertEqual(response.status_code, 200)

        json_response = response.json()

        self.assertTrue(json_response["success"])
        self.assertIn("average_rating", json_response)

        product = Product.objects.get(id=self.product.id)

        self.assertEqual(product.average_rating(), 4)

    def test_add_rating_view_product_not_found(self):
        rating_url = detail_rating_url(product_id=999)
        response = self.client.post(rating_url, {"rating": 4})

        self.assertEqual(response.status_code, 404)

        json_response = response.json()

        self.assertFalse(json_response["success"])
        self.assertEqual(json_response["error"], "Product not found")

    def test_add_rating_view_invalid_method(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)

        json_response = response.json()
        self.assertFalse(json_response["success"])
        self.assertEqual(json_response["error"], "Invalid request method")
