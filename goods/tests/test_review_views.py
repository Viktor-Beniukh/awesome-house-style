from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from goods.models import Product, Category, Review

User = get_user_model()


def detail_review_url(product_id: int):
    return reverse("catalog:review-create", args=[product_id])


class PublicReviewCreateViewTests(TestCase):

    def setUp(self) -> None:
        self.category = Category.objects.create(name="Test Category", slug="test-category")

        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=50.25,
            discount=2.0,
            quantity=2,
            category=self.category
        )

    def test_login_required(self):
        review_url = detail_review_url(self.product.id)
        response = self.client.get(review_url)

        self.assertNotEqual(response.status_code, 200)


class PrivateReviewCreateViewTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
            image_user="uploads/default.jpg"
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

        self.url = detail_review_url(self.product.id)

    def test_create_review_view_with_valid_data(self):
        form_data = {
            "text": "Test review text",
            "product": self.product.id,
            "user": self.user.id,
        }

        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.product.get_absolute_url())

        created_review = Review.objects.get(text="Test review text")

        self.assertEqual(created_review.product, self.product)
        self.assertEqual(created_review.user, self.user)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Review successfully added.")

    def test_create_review_view_with_invalid_data(self):
        form_data = {
            "text": "",
            "product": self.product.id,
            "user": self.user.id,
        }

        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.product.get_absolute_url())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Failed to add the review. Please check the form.")

        with self.assertRaises(Review.DoesNotExist):
            Review.objects.get()

    def test_create_review_view_without_login(self):
        self.client.logout()

        form_data = {
            "text": "Test review text",
            "product": self.product.id,
            "user": self.user.id,
        }

        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/user/login/?next={self.url}")

        with self.assertRaises(Review.DoesNotExist):
            Review.objects.get(text="Test review text")
