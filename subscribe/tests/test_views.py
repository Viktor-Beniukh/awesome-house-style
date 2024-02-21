from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from subscribe.models import Subscriber

User = get_user_model()


SUBSCRIBER_URL = reverse("subscribe:contact")
UNSUBSCRIBER_URL = reverse("subscribe:unsubscribe")
MAIN_URL = reverse("main:index")


class PublicSubscriberTests(TestCase):
    def test_login_required(self):
        response = self.client.get(SUBSCRIBER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateSubscriberViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com"
        )
        self.client.force_login(self.user)

    def test_subscribe_view(self):
        if not Subscriber.objects.filter(user=self.user).exists():
            data = {
                "is_subscribed": True,
                "email": self.user.email
            }

            response = self.client.post(SUBSCRIBER_URL, data)

            self.assertTrue(Subscriber.objects.filter(user=self.user).exists())

            messages = list(get_messages(response.wsgi_request))
            self.assertEqual(len(messages), 1)
            self.assertEqual(str(messages[0]), "You subscribed successfully.")

            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, MAIN_URL)
        else:
            data = {
                "is_subscribed": True,
                "email": self.user.email
            }
            response = self.client.post(SUBSCRIBER_URL, data)

            messages = list(get_messages(response.wsgi_request))
            self.assertEqual(len(messages), 1)
            self.assertEqual(str(messages[0]), "You are already subscribed.")

            self.assertEqual(response.status_code, 302)
            self.assertRedirects(response, MAIN_URL)


class PublicUnSubscriberTests(TestCase):
    def test_login_required(self):
        response = self.client.get(UNSUBSCRIBER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateUnsubscribeViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com"
        )
        self.client.force_login(self.user)
        Subscriber.objects.create(
            user=self.user,
            email=self.user.email,
            is_subscribed=True
        )

    def test_unsubscribe_view(self):
        self.assertTrue(Subscriber.objects.filter(user=self.user).exists())

        response = self.client.get(UNSUBSCRIBER_URL)

        self.assertFalse(Subscriber.objects.filter(user=self.user).exists())

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, MAIN_URL)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You have been unsubscribed.")
