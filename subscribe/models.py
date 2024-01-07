from django.conf import settings
from django.db import models


class Subscriber(models.Model):
    """Email subscription"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    is_subscribed = models.BooleanField(default=False)
    email = models.EmailField()
    date_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
