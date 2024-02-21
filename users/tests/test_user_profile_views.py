from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


MAIN_URL = reverse("main:index")
REGISTER_URL = reverse("user:register")
LOGIN_URL = reverse("user:login")
PROFILE_URL = reverse("user:profile")


class UserRegisterTests(TestCase):

    def test_user_register(self):
        response = self.client.get(REGISTER_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")

    def test_create_user(self):
        form_data = {
            "username": "new_user",
            "email": "user@test.com",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
        }

        response = self.client.post(REGISTER_URL, data=form_data)

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, MAIN_URL)

        new_user = get_user_model().objects.get(email=form_data["email"])

        self.assertEqual(new_user.username, form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])


class UserLoginTests(TestCase):

    def test_user_login(self):
        response = self.client.get(LOGIN_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")


class ProfilePublicTests(TestCase):

    def test_login_required(self):
        response = self.client.get(PROFILE_URL)

        self.assertNotEqual(response.status_code, 200)


class ProfilePrivateTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user_name",
            email="user@test.com",
            password="user12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_profile(self):
        response = self.client.get(PROFILE_URL)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "users/profile.html")
