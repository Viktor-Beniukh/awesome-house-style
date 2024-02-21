from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from goods.models import Product, Category

User = get_user_model()


MAIN_URL = reverse("main:index")
PRODUCT_CREATE_URL = reverse("catalog:create_product")


def detail_product_url(product_slug: str):
    return reverse("catalog:product", args=[product_slug])


def detail_product_update_url(product_slug: str):
    return reverse("catalog:product_update", args=[product_slug])


def detail_product_delete_url(product_slug: str):
    return reverse("catalog:product_delete", args=[product_slug])


class PublicProductViewTest(TestCase):

    def setUp(self) -> None:
        self.category = Category.objects.create(name="Test", slug="test")

        self.product = Product.objects.create(
            name="Test Product", description="Test Description", category=self.category
        )

        self.url = detail_product_url(product_slug=self.product.slug)

    def test_product_view_with_valid_product(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Test Product")
        self.assertContains(response, "Test Description")

        self.assertTemplateUsed(response, "goods/product.html")

    def test_product_view_with_invalid_product(self):
        product_url = detail_product_url(product_slug="invalid-slug")

        response = self.client.get(product_url)

        self.assertEqual(response.status_code, 404)


class PublicProductCreateViewTests(TestCase):

    def test_login_required(self):
        response = self.client.get(PRODUCT_CREATE_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateProductCreateViewTest(TestCase):

    def setUp(self) -> None:
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@user.com",
            password="adminpass"
        )
        self.admin_user.is_staff = True
        self.admin_user.save()
        self.client.force_login(self.admin_user)

        self.category = Category.objects.create(name="Test", slug="test")

        self.url = PRODUCT_CREATE_URL

    def test_product_create_view_with_admin_permission(self):
        response_get = self.client.get(self.url)

        self.assertEqual(response_get.status_code, 200)

        self.assertTemplateUsed(response_get, "goods/product_create.html")

        form_data = {
            "name": "Test Product",
            "description": "Test Description",
            "price": 50.25,
            "discount": 5.0,
            "quantity": 1,
            "category": self.category.id
        }

        response_post_valid = self.client.post(self.url, data=form_data)

        self.assertEqual(response_post_valid.status_code, 302)
        self.assertRedirects(response_post_valid, MAIN_URL)

        messages = list(get_messages(response_post_valid.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Product successfully created")

        created_product = Product.objects.get(name="Test Product")
        self.assertIsNotNone(created_product)

    def test_product_create_view_without_admin_permission(self):
        self.client.logout()

        user = User.objects.create_user(
            username="regular_user",
            email="regular@user.com",
            password="userpass"
        )
        self.client.force_login(user)

        response = self.client.get(self.url)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You do not have permission to create products.")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, MAIN_URL)


class PublicProductUpdateViewTests(TestCase):

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

        self.url = detail_product_update_url(self.product.slug)

    def test_login_required(self):
        response = self.client.get(self.url)

        self.assertNotEqual(response.status_code, 200)


class PrivateProductUpdateViewTest(TestCase):

    def setUp(self) -> None:
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@user.com",
            password="adminpass"
        )
        self.admin_user.is_staff = True
        self.admin_user.save()
        self.client.force_login(self.admin_user)

        self.category = Category.objects.create(name="Test", slug="test")

        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=50.25,
            discount=2.0,
            quantity=2,
            category=self.category
        )

        self.url = detail_product_update_url(self.product.slug)

    def test_product_update_view_with_admin_permission(self):
        response_get = self.client.get(self.url)

        self.assertEqual(response_get.status_code, 200)

        self.assertTemplateUsed(response_get, "goods/product_update.html")

        form_data = {
            "name": "Updated Product",
            "description": "Updated Description",
            "price": 75.50,
            "discount": 5.0,
            "quantity": 1,
            "category": self.category.id
        }

        response_post_valid = self.client.post(self.url, data=form_data)

        self.assertEqual(response_post_valid.status_code, 302)
        self.assertRedirects(response_post_valid, self.product.get_absolute_url())

        self.product.refresh_from_db()

        messages = list(get_messages(response_post_valid.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Product successfully updated")

        self.assertEqual(self.product.name, "Updated Product")
        self.assertEqual(self.product.description, "Updated Description")
        self.assertEqual(self.product.price, 75.50)

    def test_product_update_view_without_admin_permission(self):
        self.client.logout()

        user = User.objects.create_user(
            username="regular_user",
            email="regular@user.com",
            password="userpass"
        )
        self.client.force_login(user)

        response_get = self.client.get(self.url)

        self.assertEqual(response_get.status_code, 302)
        self.assertRedirects(response_get, self.product.get_absolute_url())

        messages = list(get_messages(response_get.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You do not have permission to update products.")


class PublicProductDeleteViewTests(TestCase):

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

        self.url = detail_product_delete_url(self.product.slug)

    def test_login_required(self):
        response = self.client.get(self.url)

        self.assertNotEqual(response.status_code, 200)


class PrivateProductDeleteViewTest(TestCase):

    def setUp(self) -> None:
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@user.com",
            password="adminpass"
        )
        self.admin_user.is_staff = True
        self.admin_user.save()
        self.client.force_login(self.admin_user)

        self.category = Category.objects.create(name="Test", slug="test")

        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=50.25,
            discount=2.0,
            quantity=2,
            category=self.category
        )

        self.url = detail_product_delete_url(self.product.slug)

    def test_product_delete_view_with_admin_permission(self):
        response_get = self.client.get(self.url)

        self.assertEqual(response_get.status_code, 200)

        self.assertTemplateUsed(response_get, "goods/product_confirm_delete.html")

        response_post = self.client.post(self.url)

        self.assertRedirects(response_post, MAIN_URL)

        messages = list(get_messages(response_post.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Product successfully removed")

        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(id=self.product.id)

    def test_product_delete_view_without_admin_permission(self):
        self.client.logout()

        user = User.objects.create_user(
            username="regular_user",
            email="regular@user.com",
            password="userpass"
        )
        self.client.force_login(user)

        response_get = self.client.get(self.url)

        self.assertEqual(response_get.status_code, 302)

        self.assertRedirects(response_get, self.product.get_absolute_url())

        messages = list(get_messages(response_get.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You do not have permission to remove products.")
