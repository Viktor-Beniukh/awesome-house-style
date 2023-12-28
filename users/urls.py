from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("profile/", views.profile_view, name="profile"),
    path("users-cart/", views.users_cart_view, name="users_cart"),
    path("logout/", views.logout_view, name="logout"),
    path("<int:pk>/password/", views.change_password_view, name="password-change"),
    path("password-success/", views.password_success_view, name="password-success"),
]
