from django.urls import path

from goods import views

app_name = "goods"

urlpatterns = [
    path("search/", views.catalog_view, name="search"),
    path("favorite-products/", views.favorite_products_view, name="favorite_products"),
    path("toggle-favorite/", views.toggle_favorite_view, name="toggle_favorite"),
    path("add-rating/<int:product_id>/", views.add_rating_view, name="add_rating"),
    path("create-category/", views.category_create_view, name="create_category"),
    path("create-product/", views.product_create_view, name="create_product"),
    path("<slug:category_slug>/", views.catalog_view, name="index"),
    path("product/<slug:product_slug>/", views.product_view, name="product"),
    path("product/<slug:product_slug>/edit/", views.product_update_view, name="product_update"),
    path("product/<slug:product_slug>/remove/", views.product_delete_view, name="product_delete"),
    path("review/<int:product_id>/", views.create_review, name="review-create"),
]
