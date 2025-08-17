from django.db import models
from django.db.models import SET_NULL

from users.models import User


# Create your models here.


# 1. Управление клиентами
class Recipient(models.Model):
    """
    Модель получателя рассылки

    Представляет клиента (получателя рассылки). Содержит email,
    Ф.И.О., комментарий
    """

    email = models.EmailField(unique=True, verbose_name="Адрес электронной почты")
    full_name = models.CharField(max_length=200, verbose_name="ФИО")
    comment = models.TextField(verbose_name="Комментарий")

    owner = models.ForeignKey(User, on_delete=SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"
        ordering = ["email"]
        db_table = "Получатели рассылки"

        # Кастомные разрешения
        permissions = [
            (
                "can_view_all_clients",
                "Can view all clients",
            ),  # Может просматривать всех клиентов
        ]


# 2. Управление сообщениями
class Message(models.Model):
    """
    Модель сообщение

    Представляет сообщение для клиента. Содержит тему письма и тело письма.
    """

    theme = models.CharField(max_length=200, verbose_name="Тема")
    body = models.TextField(verbose_name="Сообщение")
    owner = models.ForeignKey(User, on_delete=SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        db_table = "Сообщения"


# 3. Управление рассылками
class Mailing(models.Model):
    """
    Модель рассылки

    Представляет рассылку для клиента. Содержит дату и время первой отправки,
    дату и время окончания отправки, статус, сообщение и получатели
    """

    CREATED = "1"  # Рассылка была создана, но еще ни разу не была отправлена
    LAUNCHED = "2"  # Рассылка активна и была отправлена хотя бы один раз
    COMPLETED = "3"  # Время окончания отправки рассылки прошло

    date_time_of_first_mailing = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата и время первой отправки"
    )
    date_time_end_mailing = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата и время окончания отправки"
    )

    STATUS_CHOICES = [
        (CREATED, "Создана"),
        (LAUNCHED, "Активна"),
        (COMPLETED, "Завершена"),
    ]
    status = models.CharField(
        max_length=6,
        choices=STATUS_CHOICES,
        default=CREATED,
        verbose_name="Статус",
    )

    message = models.ForeignKey(
        Message,
        on_delete=models.SET_NULL,
        related_name="mailings",
        null=True,
        blank=True,
        verbose_name="Сообщение",
    )
    recipients = models.ManyToManyField(Recipient, related_name="recipients")

    # Владелец рассылки
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="mailings",
        null=True,
        blank=True,
    )

    def get_recipients(self):
        return ", ".join([recipient.email for recipient in self.recipients.all()])

    def get_recipients_for_mailing(self):
        return [recipient.email for recipient in self.recipients.all()]

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        db_table = "Рассылки"

        # Кастомные разрешения
        permissions = [
            (
                "can_disable_mailings",
                "Can disable mailings",
            ),  # Может отключить рассылки
            (
                "can_view_all_mailings",
                "Can view all mailings",
            ),  # Может просматривать все рассылки
        ]


# Создать модель "Попытка рассылки"
class AttemptToMailing(models.Model):
    """
    Модель "Попытка рассылки"

    Хранит информацию о каждой попытке рассылки. Содержит дату и время попытки,
    Статус "Успешно" или "Не успешно", Ответ почтового сервера,
    Внешний ключ на модель "Рассылка"
    """

    # Дата и время попытки
    date_time_of_attempt = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата и время попытки"
    )
    # Статус
    status = models.CharField(
        max_length=6,
        choices=[("1", "Успешно"), ("0", "Не успешно")],
        verbose_name="Статус",
        null=True,
        blank=True,
    )
    # Ответ почтового сервера
    mail_server_response = models.TextField(
        verbose_name="Ответ почтового сервера", null=True, blank=True
    )
    # Рассылка
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.SET_NULL,
        verbose_name="Рассылка",
        related_name="attempts",
        null=True,
        blank=True,
    )

    # Счетчик отправленных сообщений
    messages_count = models.PositiveIntegerField(null=True, blank=True, default=0)

    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="attempts",
        null=True,
        blank=True,
    )
