from django.urls import path

from goods import views

app_name = "goods"

urlpatterns = [
    path("search/", views.catalog_view, name="search"),
    path("create-category/", views.category_create_view, name="create_category"),
    path("<slug:category_slug>/", views.catalog_view, name="index"),
    path("product/<slug:product_slug>/", views.product_view, name="product"),
]
