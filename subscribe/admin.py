from django.contrib import admin

from subscribe.models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("user", "email", "date_at", "is_subscribed")
