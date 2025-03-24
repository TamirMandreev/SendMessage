from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

# Создать модель пользователя
class User(AbstractUser):
    # Удалить поле username
    username = None
    # Использовать email как уникальный идентификатор
    email = models.EmailField(unique=True, verbose_name="Email")

    # Определить поле email как поле для авторизации
    USERNAME_FIELD = 'email'
    # Данное поле содержит дополнительные обязательные поля, которые должны быть заполнены при создании нового пользователя
    # Список пуст, что означает, что кроме поля email никакие другие данные для регистрации нового пользователя не требуются
    REQUIRED_FIELDS = []

    # Добавить дополнительную информацию о самой модели User
    class Meta:
        # Человеко-понятное название модели в единственном числе
        verbose_name = 'Пользователь'
        # Человеко-понятное название модели во множественном числе
        verbose_name_plural = 'Пользователи'

    # Переопределить метод __str__
    def __str__(self):
        return self.email
