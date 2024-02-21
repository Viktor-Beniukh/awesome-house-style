from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from goods.models import Category

User = get_user_model()


MAIN_URL = reverse("main:index")
CATEGORY_CREATE_URL = reverse("catalog:create_category")


class PublicCategoryCreateViewTests(TestCase):

    def test_login_required(self):

        response = self.client.get(CATEGORY_CREATE_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCategoryCreateViewTest(TestCase):

    def setUp(self) -> None:
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@user.com",
            password="adminpass"
        )
        self.admin_user.is_staff = True
        self.admin_user.save()

        self.client.force_login(self.admin_user)

        self.url = CATEGORY_CREATE_URL

    def test_category_create_view_with_valid_data(self):
        response_get = self.client.get(self.url)

        self.assertEqual(response_get.status_code, 200)

        self.assertTemplateUsed(response_get, "goods/category_create.html")

        form_data = {
            "name": "Test Category",
            "slug": "test-category"
        }

        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, MAIN_URL)

        created_category = Category.objects.get(name="Test Category")

        self.assertEqual(created_category.slug, "test-category")

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Category successfully created")

    def test_category_create_view_with_invalid_data(self):
        form_data = {
            "name": "",
            "slug": "test-category"
        }

        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 200)

    def test_category_create_view_without_admin_permission(self):
        self.client.logout()

        user = User.objects.create_user(
            username="regular_user",
            email="regular@user.com",
            password="userpass"
        )
        self.client.force_login(user)

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, MAIN_URL)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), "You do not have permission to create categories."
        )
