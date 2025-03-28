from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


# Создать модель пользователя
class User(AbstractUser):
    # Удалить поле username
    username = None
    # Использовать email как уникальный идентификатор
    email = models.EmailField(unique=True, verbose_name="Email")
    # Аватар
    image = models.ImageField(upload_to="users/photo", verbose_name="Аватар", blank=True, null=True)
    # Телефон
    phone = models.CharField(max_length=35, blank=True, null=True, verbose_name='Телефон')
    # Страна
    country = models.CharField(max_length=255, blank=True, null=True, verbose_name='Страна')
    # Токен нужен для подтверждения учетной записи по электронной почте
    token = models.CharField(
        max_length=100, verbose_name="Token", blank=True, null=True
    )
    reset_token = models.CharField(
        max_length=100, verbose_name="Reset Token", blank=True, null=True
    )

    # Определить поле email как поле для авторизации
    USERNAME_FIELD = "email"
    # Данное поле содержит дополнительные обязательные поля, которые
    # должны быть заполнены при создании нового пользователя
    # Список пуст, что означает, что кроме поля email никакие другие
    # данные для регистрации нового пользователя не требуются
    REQUIRED_FIELDS = []

    # Добавить дополнительную информацию о самой модели User
    class Meta:
        # Человеко-понятное название модели в единственном числе
        verbose_name = "Пользователь"
        # Человеко-понятное название модели во множественном числе
        verbose_name_plural = "Пользователи"

        # Кастомные разрешения
        permissions = [
            (
                "can_view_all_users",
                "Can view all users",
            ),  # Может просматривать всех пользователей
            (
                "can_block_users",
                "Can block users",
            ),  # Может блокировать пользователей
        ]

    # Переопределить метод __str__
    def __str__(self):
        return self.email
