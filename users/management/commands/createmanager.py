# BaseCommand позволяет создавать команды для командной строки
from django.core.management import BaseCommand
from django.contrib.auth.models import Group

from users.models import User


# Создать команду для создания менеджера
class Command(BaseCommand):
    # Метод handle является основным методом, который выполняется
    # при запуске команды
    def handle(self, *args, **options):
        # Запросить у пользователя email
        email = input("Email: ")
        # Запросить у пользователя пароль
        password1 = input("Пароль: ")
        # Запросить у пользователя пароль 2
        password2 = input("Повторите пароль: ")
        # Если пароли совпадают
        if password1 == password2:
            # Создать объект пользователя
            user = User.objects.create(email=email)
            # Установить пароль
            user.set_password(password1)
            # Активировать пользователя
            user.is_active = True
            # Назначить права администратора
            user.is_staff = True

            # Добавить пользователя в группу "Менеджеры"
            user.groups.add(Group.objects.get(name="Менеджеры"))

            # Сохранить пользователя
            user.save()
        else:
            self.stderr.write("Неправильный пароль")
