from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from goods.models import Category, Product, Review, Rating


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name="Test", slug="test")

    def test_category_str(self):
        category = Category.objects.get(id=1)
        self.assertEqual(str(category), category.name)

    def test_save_category_with_valid_data(self):
        category = Category(name="Test Category")
        category.save()
        self.assertTrue(category.id)
        self.assertEqual(category.slug, "test-category")

    def test_save_category_with_duplicate_slug(self):
        Category.objects.create(name="Test Category")

        with self.assertRaises(IntegrityError):
            Category.objects.create(name="Test Category")


class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name="Test", slug="test")
        Product.objects.create(
            name="Product",
            slug="product",
            price=100.0,
            discount=10.0,
            category=category
        )

    def test_product_str(self):
        product = Product.objects.get(id=1)
        self.assertEqual(str(product), product.name)

    def test_get_absolute_url(self):
        product = Product.objects.get(id=1)
        expected_url = reverse("catalog:product", kwargs={"product_slug": product.slug})
        self.assertEqual(product.get_absolute_url(), expected_url)

    def test_display_id(self):
        product = Product.objects.get(id=1)
        self.assertEqual(product.display_id(), f"{product.pk:05}")

    def test_sell_price_with_discount(self):
        product = Product.objects.get(id=1)
        self.assertEqual(product.sell_price(), 90.00)

    def test_average_rating_no_ratings(self):
        product = Product.objects.get(id=1)
        self.assertEqual(product.average_rating(), 0)

    def test_get_review(self):
        user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass",
        )
        product = Product.objects.get(id=1)
        review = Review.objects.create(user=user, product=product, text="Test")

        self.assertEqual(list(product.get_review()), [review])

    def test_save_product_with_valid_data(self):
        category = Category.objects.create(name="Test Category")
        product = Product(name="Test Product", category=category)
        product.save()
        self.assertTrue(product.id)
        self.assertEqual(product.slug, "test-product")

    def test_save_product_with_duplicate_slug(self):
        category = Category.objects.create(name="Test Category")
        Product.objects.create(name="Test Product", category=category)

        with self.assertRaises(IntegrityError):
            Product.objects.create(name="Test Product", category=category)


class ReviewModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create(
            email="admin@user.com",
            password="admin12345",
            username="Admin"
        )
        category = Category.objects.create(
            name="Test",
            slug="test"
        )
        product = Product.objects.create(
            name="Product",
            slug="product",
            category=category
        )

        Review.objects.create(user=user, product=product)

    def test_review_str(self):
        review = Review.objects.get(id=1)

        self.assertEqual(str(review), f"{review.user} - {review.product}")


class RatingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create(
            email="admin@user.com",
            password="admin12345",
            username="Admin"
        )
        category = Category.objects.create(
            name="Test",
            slug="test"
        )
        product = Product.objects.create(
            name="Product",
            slug="product",
            category=category
        )

        Rating.objects.create(user=user, product=product, rating=5)

    def test_rating_str(self):
        rating = Rating.objects.get(id=1)

        self.assertEqual(str(rating), f"{rating.rating} - {rating.product}")
