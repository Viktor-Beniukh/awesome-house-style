from django.test import TestCase, Client
from django.urls import reverse


class MainViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse("main:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/index.html")
        self.assertContains(response, "House Style - Home Page")
