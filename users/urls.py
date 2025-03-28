from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users import views
from users.apps import UsersConfig

# Задать имя приложения в пространстве имен (namespace)
app_name = UsersConfig.name

urlpatterns = [
    path("register/", views.UserCreateView.as_view(), name="register"),
    path(
        "login/",
        LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "email-confirm/<str:token>/",
        views.email_verifivation,
        name="email_confirm",
    ),
    path(
        "password-reset-request/",
        views.PasswordResetRequestView.as_view(),
        name="password_reset_request",
    ),
    path(
        "password_reset_confirm/",
        views.PasswordResetView.as_view(),
        name="password_reset_confirm",
    ),
    path("list/", views.UsersListView.as_view(), name="users_list"),
    path("detail/<int:pk>", views.UserDetailView.as_view(), name="user_detail"),
    path("update/<int:pk>", views.UserUpdateView.as_view(), name="user_update"),
    path("block/<int:pk>", views.block_user, name="user_block"),
]
