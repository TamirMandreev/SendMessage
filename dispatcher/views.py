from django.http import HttpResponseRedirect
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.views.generic.detail import SingleObjectMixin

from dispatcher.forms import RecipientForm, MessageForm, MailingForm
from dispatcher.models import Recipient, Message, Mailing, AttemptToMailing


# Create your views here.
# 1. Управление клиентами

class RecipientListView(ListView):
    '''
    Представление для отображения всех получателей рассылки (клиентов)
    '''
    model = Recipient
    template_name = 'dispatcher/recipients_list.html'
    context_object_name = 'recipients'


class RecipientCreateView(CreateView):
    '''
    Представление для создания получателей рассылки (клиентов)
    '''
    model = Recipient
    form_class = RecipientForm
    template_name = 'dispatcher/recipient_form.html'
    success_url = reverse_lazy('dispatcher:recipients_list')


class RecipientUpdateView(UpdateView):
    '''
    Представление для редактирования получателя рассылки (клиента)
    '''
    model = Recipient
    form_class = RecipientForm
    template_name = 'dispatcher/recipient_form.html'
    success_url = reverse_lazy('dispatcher:recipients_list')


class RecipientDetailView(DetailView):
    '''
    Представление для просмотра детальной информации о получателе рассылки (клиенте)
    '''
    model = Recipient
    template_name = 'dispatcher/recipient_detail.html'
    context_object_name = 'recipient'



class RecipientDeleteView(DeleteView):
    '''
    Представление для удаления получателя рассылки (клиента)
    '''
    model = Recipient
    template_name = 'dispatcher/recipient_delete.html'
    success_url = reverse_lazy('dispatcher:recipients_list')


# 2. Управление сообщениями

class MessageCreateView(CreateView):
    '''
    Представление для создания сообщения
    '''
    model = Message
    form_class = MessageForm
    template_name = 'dispatcher/message_form.html'
    success_url = reverse_lazy('dispatcher:messages_list')


class MessageListView(ListView):
    '''
    Представление для отображения всех сообщений
    '''
    model = Message
    template_name = 'dispatcher/messages_list.html'
    context_object_name = 'messages'

class MessageDetailView(DetailView):
    '''
    Представление для отображения подробной информации о сообщении
    '''
    model = Message
    template_name = 'dispatcher/message_detail.html'
    context_object_name = 'message'


class MessageUpdateView(UpdateView):
    '''
    Представление для редактирования сообщения
    '''
    model = Message
    form_class = MessageForm
    template_name = 'dispatcher/message_form.html'
    success_url = reverse_lazy('dispatcher:messages_list')


class MessageDeleteView(DeleteView):
    '''
    Представление для удаления сообщения
    '''
    model = Message
    template_name = 'dispatcher/message_delete.html'
    success_url = reverse_lazy('dispatcher:messages_list')


# 3. Управление рассылками
class MailingCreateView(CreateView):
    '''
    Представление для создания рассылки
    '''
    model = Mailing
    form_class = MailingForm
    template_name = 'dispatcher/mailing_form.html'
    success_url = reverse_lazy('dispatcher:mailings_list')


class MailingListView(ListView):
    '''
    Представление для отображения всех рассылок
    '''
    model = Mailing
    template_name = 'dispatcher/mailings_list.html'
    context_object_name = 'mailings'


class MailingDetailView(DetailView):
    '''
    Представление для отображения подробной информации о рассылке
    '''
    model = Mailing
    template_name = 'dispatcher/mailing_detail.html'
    context_object_name = 'mailing'


class MailingUpdateView(UpdateView):
    '''
    Представление для редактирования рассылки
    '''
    model = Mailing
    form_class = MailingForm
    template_name = 'dispatcher/mailing_form.html'
    success_url = reverse_lazy('dispatcher:mailings_list')


class MailingDeleteView(DeleteView):
    '''
    Представление для удаления рассылки
    '''
    model = Mailing
    template_name = 'dispatcher/mailing_delete.html'
    success_url = reverse_lazy('dispatcher:mailings_list')


# SingleIbjectMixin позволяет получать объект модели по идентификатору (id)
class MailingStartView(TemplateView, SingleObjectMixin):
    '''
    Представление для обработки POST-запроса на запуск рассылки
    '''
    # Указать модель, с которой будет работать представление
    model = Mailing
    # Указать имя аргумента URL, который содержит первичный ключ объекта
    pk_url_kwarg = 'pk'
    template_name = 'dispatcher/mailing_detail.html'
    context_object_name = 'mailing'

    # Метод post обрабатывает POST-запросы. Он вызывается, когда форма отправляется методом POST
    def post(self, request, *args, **kwargs):
        # Получить объект модели Mailing по переданному id
        mailing = self.get_object()
        # Обновить статус рассылки
        mailing.status = mailing.LAUNCHED
        # Записать дату и время первой отправки
        if not mailing.date_time_of_first_mailing:
            mailing.date_time_of_first_mailing = timezone.now()
        # Сохранить изменения в базу данных
        mailing.save()

        # Создать объект модели AttemptToMailing
        attempt = AttemptToMailing.objects.create(date_time_of_attempt=timezone.now(), mailing=mailing)

        from django.core.mail import send_mail
        try:
            # Отправить сообщения
            send_mail(
                subject=mailing.message.theme, # Тема письма
                message=mailing.message.body, # Тело письма
                from_email=EMAIL_HOST_USER, # Адрес отправителя
                recipient_list=mailing.get_recipients_for_mailing() # Список получателей
            )
            # Установить статус отправки "Успешно"
            attempt.status = '1'
        except Exception as e:
            # Установить статус отправки "Не успешно"
            attempt.status = '0'
            # Записать информацию об ошибке в "Ответ почтового сервера"
            attempt.mail_server_response = e

        # Сохранить attempt
        attempt.save()

        # Записать дату и время окончания отправки
        mailing.date_time_end_mailing = timezone.now()
        # Обновить статус рассылки
        mailing.status = mailing.COMPLETED
        # Сохранить изменения
        mailing.save()

        # После успешной отправки письма перенаправить пользователя обратно на страницу подробной информации о рассылке
        return HttpResponseRedirect(reverse_lazy('dispatcher:mailing_detail', kwargs={'pk': mailing.pk}))