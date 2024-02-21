from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse

from subscribe.models import Subscriber

User = get_user_model()


class SubscribeViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com"
        )
        self.client = Client()
        self.client.force_login(self.user)

    def test_subscribe_view(self):
        if not Subscriber.objects.filter(user=self.user).exists():
            data = {
                "is_subscribed": True,
                "email": self.user.email
            }
            response = self.client.post(reverse("subscribe:contact"), data)

            self.assertTrue(Subscriber.objects.filter(user=self.user).exists())

            messages = list(get_messages(response.wsgi_request))
            self.assertEqual(len(messages), 1)
            self.assertEqual(str(messages[0]), "You subscribed successfully.")

            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("main:index"))
        else:
            data = {
                "is_subscribed": True,
                "email": self.user.email
            }
            response = self.client.post(reverse("subscribe:contact"), data)

            messages = list(get_messages(response.wsgi_request))
            self.assertEqual(len(messages), 1)
            self.assertEqual(str(messages[0]), "You are already subscribed.")

            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, reverse("main:index"))


class UnsubscribeViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com"
        )
        Subscriber.objects.create(
            user=self.user,
            email=self.user.email,
            is_subscribed=True
        )
        self.client = Client()
        self.client.force_login(self.user)

    def test_unsubscribe_view(self):
        self.assertTrue(Subscriber.objects.filter(user=self.user).exists())

        response = self.client.get(reverse("subscribe:unsubscribe"))

        self.assertFalse(Subscriber.objects.filter(user=self.user).exists())

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("main:index"))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You have been unsubscribed.")
