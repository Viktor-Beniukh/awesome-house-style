from django.urls import path

from goods import views

app_name = "goods"

urlpatterns = [
    path("search/", views.catalog_view, name="search"),
    path("create-category/", views.category_create_view, name="create_category"),
    path("create-product/", views.product_create_view, name="create_product"),
    path("<slug:category_slug>/", views.catalog_view, name="index"),
    path("product/<slug:product_slug>/", views.product_view, name="product"),
    path("product/<slug:product_slug>/edit/", views.product_update_view, name="product_update"),
    path("product/<slug:product_slug>/remove/", views.product_delete_view, name="product_delete"),
]
