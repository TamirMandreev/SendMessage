from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserRegisterForm
from users.models import User


# Create your views here.

# Создать представление для создания пользователя (Объекта модели User)
class UserCreateView(CreateView):
    # Указать модель, с которой будет работать представлением
    model = User
    # Указать шаблон, который будет использоваться для отображения формы
    template_name = 'users/user_create.html'
    # Интегрировать (подключить) form_class
    form_class = UserRegisterForm
    # Определить URL-адрес, на который будет перенаправлен пользователь после успешной отправки формы
    success_url = reverse_lazy('users:login')