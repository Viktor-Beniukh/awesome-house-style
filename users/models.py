import os
import uuid

from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField


def user_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.username)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/user_pics/", filename)


class User(AbstractUser):
    image_user = models.ImageField(upload_to=user_image_file_path, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)

    def __str__(self):
        return self.username

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        super().save()

        if self.image_user:
            img = Image.open(self.image_user.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image_user.path)
