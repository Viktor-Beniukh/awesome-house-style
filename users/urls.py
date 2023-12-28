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
    path(
        "reset_password/", views.reset_password_view, name="reset_password"
    ),
    path(
        "reset_password_sent/", views.reset_password_done_view, name="password_reset_done"
    ),
    path(
        "reset/<uidb64>/<token>/", views.reset_password_confirm_view, name="password_reset_confirm"
    ),
    path(
        "reset_password_complete/", views.reset_password_complete_view, name="password_reset_complete"
    ),
]
