from django.contrib.auth import get_user_model
from django.test import TestCase

from subscribe.forms import SubscribeForm


User = get_user_model()


class SubscribeFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com"
        )

    def test_form_with_valid_data(self):
        form_data = {
            "is_subscribed": True,
            "email": self.user.email,
        }
        form = SubscribeForm(user=self.user, data=form_data)
        self.assertTrue(form.is_valid())

        instance = form.save()
        self.assertEqual(instance.user, self.user)
        self.assertEqual(instance.is_subscribed, True)
        self.assertEqual(instance.email, self.user.email)

    def test_form_with_invalid_data(self):
        form_data = {
            "is_subscribed": True,
            "email": "invalid_email",
        }
        form = SubscribeForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())

        form_data = {
            "is_subscribed": True,
        }
        form = SubscribeForm(user=self.user, data=form_data)
        self.assertFalse(form.is_valid())
