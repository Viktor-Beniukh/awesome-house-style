from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()

REGISTER_URL = reverse("user:register")
LOGIN_URL = reverse("user:login")
PROFILE_URL = reverse("user:profile")
RESET_PASSWORD_URL = reverse("user:reset_password")


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

        self.client.post(REGISTER_URL, data=form_data)
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


class ChangePasswordViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user_name",
            email="user@test.com",
            password="user12345"
        )
        self.client.force_login(self.user)
        self.url = reverse("user:password-change", kwargs={"pk": self.user.pk})

    def test_change_password_view_render(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/password_change_form.html")

    def test_change_password_form_valid(self):
        data = {
            "old_password": "user12345",
            "new_password1": "newpass123",
            "new_password2": "newpass123",
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse("user:password-success"))

        updated_user = get_user_model().objects.get(pk=self.user.pk)
        self.assertTrue(updated_user.check_password("newpass123"))

        invalid_login = self.client.login(username=self.user.email, password="user12345")
        self.assertFalse(invalid_login)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Password changed successfully.")

    def test_change_password_form_invalid(self):
        data = {
            "old_password": "user12345",
            "new_password1": "newpass123",
            "new_password2": "differentpass",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"], "new_password2", "The two password fields didn’t match."
        )


class ResetPasswordViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user_name",
            email="user@test.com",
            password="user12345"
        )
        self.url = RESET_PASSWORD_URL

    def test_reset_password_view_render(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/password_reset_form.html")

    def test_reset_password_valid(self):
        link = reverse("user:password_reset_confirm", args=["base64uid", "token"])
        response = self.client.post(self.url, {"email": "user@test.com"})
        self.assertRedirects(response, reverse("user:password_reset_done"))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Message sent successfully.")

    def test_reset_password_invalid(self):
        response = self.client.post(self.url, {"email": "invalid-email"})

        self.assertEqual(response.status_code, 200)

        form_errors = response.context["form"].errors
        self.assertEqual(form_errors["email"], ["Enter a valid email address."])


class PasswordResetConfirmViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            email="test@example.com",
            password="test_password"
        )
        self.token = default_token_generator.make_token(self.user)
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))

    def test_reset_password_confirm_view_valid(self):
        url = reverse(
            "user:password_reset_confirm",
            kwargs={"uidb64": self.uidb64, "token": self.token}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertIn("form", response.context)

        form = response.context["form"]
        self.assertIsNotNone(form)
        self.assertIsInstance(form, SetPasswordForm)

    def test_reset_password_confirm_view_invalid_token(self):
        url = reverse(
            "user:password_reset_confirm",
            kwargs={"uidb64": self.uidb64, "token": "invalid-token"}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        context = response.context[-1]
        self.assertIsNone(context.get("form"))

    def test_reset_password_confirm_view_invalid_uid(self):
        invalid_uid = "invalid-uid".encode("utf-8")
        invalid_uidb64 = urlsafe_base64_encode(invalid_uid)

        url = reverse(
            "user:password_reset_confirm",
            kwargs={"uidb64": invalid_uidb64, "token": self.token}
        )

        with self.assertRaises(ValueError) as cm:
            self.client.get(url, follow=True)

        self.assertEqual(
            str(cm.exception), "Field 'id' expected a number but got 'invalid-uid'."
        )

    def test_reset_password_confirm_view_invalid_user(self):
        url = reverse(
            "user:password_reset_confirm",
            kwargs={"uidb64": urlsafe_base64_encode(force_bytes(999)), "token": self.token}
        )
        with self.assertRaises(User.DoesNotExist):
            self.client.get(url)
