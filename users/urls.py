from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users import views
from users.apps import UsersConfig

# Задать имя приложения в пространстве имен (namespace)
app_name = UsersConfig.name

urlpatterns = [
    path('register/', views.UserCreateView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]