from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from dispatcher.forms import RecipientForm, MessageForm, MailingForm
from dispatcher.models import Recipient, Message, Mailing


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