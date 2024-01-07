from django.urls import path

from orders import views

app_name = "orders"

urlpatterns = [
    path("create-order/", views.create_order_view, name="create_order"),
    path(
        "<int:pk>/create-checkout-session/",
        views.create_checkout_session,
        name="create-checkout-session"
    ),
    path("success/", views.success_view, name="success"),
    path("cancel/", views.cancel_view, name="cancel"),
]
