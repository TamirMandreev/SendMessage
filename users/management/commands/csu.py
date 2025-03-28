# BaseCommand позволяет создавать команды для командной строки
from django.core.management import BaseCommand

from users.models import User


# Создать команду для создания суперпользователя
class Command(BaseCommand):
    # Метод handle является основным методом, который
    # выполняется при запуске команды
    def handle(self, *args, **options):
        # Создать объект пользователя
        user = User.objects.create(email="tamirmandreev@example.com")
        # Установить пароль
        user.set_password("1234")
        # Активировать пользователя
        user.is_active = True
        # Назначить права администратора
        user.is_staff = True
        # Наделить пользотеля правами суперпользователя
        user.is_superuser = True
        # Сохранить пользователя
        user.save()
