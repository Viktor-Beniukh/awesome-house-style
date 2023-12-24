# Generated by Django 4.2.8 on 2023-12-23 18:40

from django.db import migrations, models
import django.db.models.deletion
import goods.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=255, unique=True)),
                ("slug", models.SlugField(max_length=255, unique=True)),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
                "ordering": ("name",),
                "index_together": {("id", "slug")},
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=255)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                (
                    "image_product",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=goods.models.product_image_file_path,
                    ),
                ),
                ("description", models.TextField(blank=True)),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                (
                    "discount",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
                ),
                ("quantity", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="goods.category",
                    ),
                ),
            ],
            options={
                "ordering": ("name",),
                "index_together": {("id", "slug")},
            },
        ),
    ]