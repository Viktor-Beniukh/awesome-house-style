import os
import uuid

from django.db import models
from django.utils.text import slugify


def product_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/products/", filename)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        index_together = (("id", "slug"),)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    image_product = models.ImageField(
        upload_to=product_image_file_path, blank=True, null=True
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        to=Category, on_delete=models.CASCADE, related_name="products"
    )

    class Meta:
        ordering = ("id",)
        index_together = (("id", "slug"),)

    def __str__(self):
        return self.name

    def display_id(self):
        return f"{self.id:05}"

    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)

        return self.price
