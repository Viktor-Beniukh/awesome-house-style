from django.urls import path

from subscribe.views import SubscribeView, UnsubscribeView


app_name = "subscribe"


urlpatterns = [
    path("contact/", SubscribeView.as_view(), name="contact"),
    path("unsubscribe/", UnsubscribeView.as_view(), name="unsubscribe"),
]
