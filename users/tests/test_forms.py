from django.contrib.auth import get_user_model
from django.test import TestCase

from users.forms import UserRegisterForm, UserLoginForm, UserProfileForm


class UserFormTests(TestCase):
    def test_user_creation_register_form_is_valid(self):
        form_data = {
            "username": "new_user",
            "email": "user@test.com",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
        }

        form = UserRegisterForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_user_register_form_password_mismatch(self):
        form_data = {
            "username": "new_user",
            "email": "user@test.com",
            "password1": "user123test",
            "password2": "mismatched_password",
            "first_name": "Test first",
            "last_name": "Test last",
        }

        form = UserRegisterForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_user_profile_form_is_valid(self):
        form_data = {
            "username": "new_user",
            "email": "user@test.com",
            "first_name": "Test first",
            "last_name": "Test last",
        }
        form = UserProfileForm(data=form_data)

        self.assertTrue(form.is_valid())


class UserLoginTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user_name",
            email="user@test.com",
            password="user123test"
        )

    def test_user_login_form_is_valid(self):
        form_data = {
            "username": "user@test.com",
            "password": "user123test",
        }
        form = UserLoginForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_user_login_form_invalid_credentials(self):
        form_data = {
            "username": "user@test.com",
            "password": "wrong_password",
        }
        form = UserLoginForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
