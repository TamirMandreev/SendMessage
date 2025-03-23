from django.db import models

# Create your models here.

# 1. Управление клиентами
class Recipient(models.Model):
    '''
    Модель получателя рассылки

    Представляет клиента (получателя рассылки). Содержит email,
    Ф.И.О., комментарий
    '''

    email = models.EmailField(unique=True, verbose_name='Адрес электронной почты')
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    comment = models.TextField(verbose_name='Комментарий')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Получатель рассылки'
        verbose_name_plural = 'Получатели рассылки'
        ordering = ['email']
        db_table = 'Получатели рассылки'


# 2. Управление сообщениями
class Message(models.Model):
    '''
    Модель сообщение

    Представляет сообщение для клиента. Содержит тему письма и тело письма.
    '''
    theme = models.CharField(max_length=200, verbose_name='Тема')
    body = models.TextField(verbose_name='Сообщение')

    def __str__(self):
        return self.theme

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        db_table = 'Сообщения'



# 3. Управление рассылками
class Mailing(models.Model):
    '''
    Модель рассылки

    Представляет рассылку для клиента. Содержит дату и время первой отправки,
    дату и время окончания отправки, статус, сообщение и получатели
    '''
    CREATED = '1' # Рассылка была создана, но еще ни разу не была отправлена
    LAUNCHED = '2' # Рассылка активна и была отправлена хотя бы один раз
    COMPLETED = '3' # Время окончания отправки рассылки прошло

    date_time_of_first_mailing = models.DateTimeField(null=True, blank=True, verbose_name='Дата и время первой отправки')
    date_time_end_mailing = models.DateTimeField(null=True, blank=True, verbose_name='Дата и время окончания отправки')

    STATUS_CHOICES = [
        (CREATED, 'Создана'),
        (LAUNCHED, 'Активна'),
        (COMPLETED, 'Завершена')
    ]
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default=CREATED, verbose_name='Статус')

    message = models.ForeignKey(Message, on_delete=models.SET_NULL, related_name='mailings', null=True, blank=True, verbose_name='Сообщение')
    recipients = models.ManyToManyField(Recipient, related_name='recipients')

    def get_recipients(self):
        return ', '.join([recipient.email for recipient in self.recipients.all()])

    def get_recipients_for_mailing(self):
        return [recipient.email for recipient in self.recipients.all()]

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        db_table = 'Рассылки'



