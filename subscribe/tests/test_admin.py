from django.test import TestCase
from django.contrib.admin.sites import AdminSite

from subscribe.admin import SubscriberAdmin
from subscribe.models import Subscriber


class SubscriberAdminTest(TestCase):
    def setUp(self):
        self.admin_site = AdminSite()
        self.subscriber_admin = SubscriberAdmin(Subscriber, self.admin_site)

    def test_list_display(self):
        expected_list_display = ("user", "email", "date_at", "is_subscribed")
        self.assertEqual(self.subscriber_admin.list_display, expected_list_display)
