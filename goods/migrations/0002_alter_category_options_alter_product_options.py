# Generated by Django 4.2.8 on 2023-12-24 20:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("goods", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={
                "ordering": ("id",),
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.AlterModelOptions(
            name="product",
            options={"ordering": ("id",)},
        ),
    ]