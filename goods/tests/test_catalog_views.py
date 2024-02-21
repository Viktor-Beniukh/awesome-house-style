from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from goods.models import Product, Category


User = get_user_model()


def detail_catalog_url(category_slug: str):
    return reverse("catalog:index", args=[category_slug])


class PublicCatalogViewTest(TestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(name="Test", slug="test")
        self.product1 = Product.objects.create(
            name="Product 1", description="Description 1", category=self.category
        )
        self.product2 = Product.objects.create(
            name="Product 2", description="Description 2", category=self.category
        )

        self.url = detail_catalog_url(self.category.slug)

    def test_catalog_view_with_products(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.product1.name)
        self.assertContains(response, self.product2.name)

        self.assertTemplateUsed(response, "goods/catalog.html")

    def test_catalog_view_without_products(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "No products available", count=0)

        self.assertTemplateUsed(response, "goods/catalog.html")
