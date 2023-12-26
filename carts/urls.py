from django.urls import path

from carts import views

app_name = "carts"

urlpatterns = [
    path("cart_add/<slug:product_slug>/", views.cart_add_view, name="cart_add"),
    path("cart_change/<slug:product_slug>/", views.cart_change_view, name="cart_change"),
    path("cart_remove/<int:cart_id>/", views.cart_remove_view, name="cart_remove"),
]
