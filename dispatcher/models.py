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



