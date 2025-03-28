from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from dispatcher.models import Mailing


# Создать кастомную команду для отправки рассылки
class Command(BaseCommand):
    """
    Команда запускает рассылку по идентификатору

    python3 manage.py mailing_start mailing.id
    """

    # Добавить обязательный аргумент mailing_id в командную строку
    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int, help="Mailing ID")

    # Прописать основную логику команды
    def handle(self, *args, **options):
        # Получить аргумент mailing_id из словаря options
        mailing_id = options["mailing_id"]
        # Получить объект модели Mailing
        mailing = get_object_or_404(Mailing, id=mailing_id)

        # Обновить статус рассылки
        mailing.status = mailing.LAUNCHED
        # Записать дату и время первой отправки
        if not mailing.date_time_of_first_mailing:
            mailing.date_time_of_first_mailing = timezone.now()
        # Сохранить изменения в базу данных
        mailing.save()

        from django.core.mail import send_mail

        # Отправить сообщения
        send_mail(
            subject=mailing.message.theme,  # Тема письма
            message=mailing.message.body,  # Тело письма
            from_email=EMAIL_HOST_USER,  # Адрес отправителя
            # Список получателей
            recipient_list=mailing.get_recipients_for_mailing(),
        )

        # Записать дату и время окончания отправки
        mailing.date_time_end_mailing = timezone.now()
        # Обновить статус рассылки
        mailing.status = mailing.COMPLETED
        # Сохранить изменения
        mailing.save()

        # Вывести в консоль сообщение о завершении отправки рассылки
        self.stdout.write(
            self.style.SUCCESS(
                f"Рассылка с идентификатором {mailing_id} успешно отправлена"
            )
        )
