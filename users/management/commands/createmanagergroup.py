from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission


# Создать команду для создания менеджера
class Command(BaseCommand):
    # Метод handle является основным методом, который выполняется
    # при запуске команды
    def handle(self, *args, **options):
        # Создать группу "Менеджеры"
        managers_group = Group.objects.create(name="Менеджеры")
        # Получить разрешения необходимые для группы разрешения
        can_disable_mailings = Permission.objects.get(
            codename="can_disable_mailings"
        )
        can_view_all_mailings = Permission.objects.get(
            codename="can_view_all_mailings"
        )
        can_view_all_clients = Permission.objects.get(
            codename="can_view_all_clients"
        )
        can_block_users = Permission.objects.get(codename="can_block_users")
        can_view_all_users = Permission.objects.get(
            codename="can_view_all_users"
        )

        # Добавить полученные разрешения группе "Менеджеры"
        managers_group.permissions.add(
            can_disable_mailings,
            can_view_all_mailings,
            can_view_all_clients,
            can_view_all_users,
            can_block_users,
        )
        # Сохранить группу
        managers_group.save()
