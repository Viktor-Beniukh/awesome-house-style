from django.contrib.auth import get_user_model
from django.test import TestCase

from goods.forms import CategoryForm, ProductForm, ReviewForm
from goods.models import Category


class GoodsFormTests(TestCase):
    def test_category_creation_form_is_valid(self):
        form_data = {
            "name": "Test",
        }

        form = CategoryForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_category_creation_form_required_fields(self):
        form_data = {
            "name": "",
        }

        form = CategoryForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_product_creation_form_is_valid(self):
        category = Category.objects.create(
            name="Test",
            slug="test"
        )
        form_data = {
            "name": "Product",
            "description": "Product description",
            "price": "50.25",
            "discount": "5.00",
            "quantity": 2,
            "category": category,
        }

        form = ProductForm(data=form_data)

        self.assertTrue(form.is_valid())

        cleaned_data = form.cleaned_data

        self.assertEqual(cleaned_data["name"], form_data["name"])
        self.assertEqual(cleaned_data["description"], form_data["description"])
        self.assertEqual(str(cleaned_data["price"]), form_data["price"])
        self.assertEqual(str(cleaned_data["discount"]), form_data["discount"])
        self.assertEqual(cleaned_data["quantity"], form_data["quantity"])
        self.assertEqual(cleaned_data["category"], form_data["category"])

    def test_product_creation_form_required_fields(self):
        form_data = {
            "name": "Product",
            "description": "Product description",
            "price": "",
            "discount": "",
            "quantity": "",
            "category": None,
        }

        form = ProductForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("price", form.errors)
        self.assertIn("discount", form.errors)
        self.assertIn("quantity", form.errors)
        self.assertIn("category", form.errors)


class ReviewFormTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user_name",
            email="user@test.com",
            password="user123test"
        )

    def test_review_form_is_valid(self):
        form_data = {
            "user": self.user,
            "text": "text",
        }
        form = ReviewForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_review_form_required_fields(self):
        form_data = {
            "user": None,
            "text": "",
        }

        form = ReviewForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("user", form.errors)
        self.assertIn("text", form.errors)

    def test_review_form_text_field(self):
        form_data = {
            "user": self.user,
            "text": "  ",
        }

        form = ReviewForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("text", form.errors)
