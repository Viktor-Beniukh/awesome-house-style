# Generated by Django 4.2.8 on 2023-12-24 20:16

from django.db import migrations, models
import phonenumber_field.modelfields
import users.models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="image_user",
            field=models.ImageField(
                blank=True, null=True, upload_to=users.models.user_image_file_path
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True, max_length=128, null=True, region=None
            ),
        ),
    ]