from django.urls import path

from goods import views

app_name = "goods"

urlpatterns = [
    path("", views.catalog, name="index"),
    path("product/<slug:product_slug>/", views.product_view, name="product"),
]
