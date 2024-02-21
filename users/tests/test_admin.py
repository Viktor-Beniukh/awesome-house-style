from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from users.admin import UserAdmin
from users.models import User


class AdminSiteTests(TestCase):

    def setUp(self) -> None:
        self.admin_site = AdminSite()
        self.user_admin = UserAdmin(User, self.admin_site)
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@user.com",
            password="admin12345"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            username="user_name",
            email="test@user.com",
            password="user12345",
            phone_number="+987654321023",
            first_name="test",
            last_name="user",
            image_user="uploads/default.jpg"
        )

    def test_list_display(self):
        expected_list_display = UserAdmin.list_display
        self.assertEqual(self.user_admin.list_display, expected_list_display)

    def test_user_phone_number_listed(self):
        """
        Tests that user's phone number is in list_display on user admin page
        """

        url = reverse("admin:users_user_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.user.phone_number)

    def test_user_create_additional_fields_listed(self):
        """
        Tests that user's additional fields (first name, last name, phone number, image_user) is on user detail admin page
        """

        url = reverse("admin:users_user_change", args=[self.user.id])
        response = self.client.get(url)

        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.last_name)
        self.assertContains(response, self.user.phone_number)
        self.assertContains(response, self.user.image_user)

    def test_user_create_additional_fields_added_user(self):
        """
        Tests that user's additional fields (first name, last name, phone number, image_user, email)
        are added to the user creation page
        """

        url = reverse("admin:users_user_add")
        response = self.client.get(url)

        self.assertContains(response, 'name="first_name"')
        self.assertContains(response, 'name="last_name"')
        self.assertContains(response, 'name="phone_number"')
        self.assertContains(response, 'name="image_user"')
        self.assertContains(response, 'name="email"')
