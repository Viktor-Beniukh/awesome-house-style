from django.contrib.auth import get_user_model
from django.test import TestCase

from subscribe.models import Subscriber


class SubscriberModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        user = get_user_model().objects.create_user(
            email="admin@user.com",
            password="admin12345",
            username="Admin"
        )
        Subscriber.objects.create(user=user, email=user.email)

    def test_subscriber_str(self):
        subscriber = Subscriber.objects.get(id=1)
        self.assertEqual(str(subscriber), subscriber.email)
