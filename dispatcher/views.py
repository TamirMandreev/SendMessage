from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from dispatcher.forms import RecipientForm
from dispatcher.models import Recipient


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


class RecipientDeleteView(DeleteView):
    '''
    Представление для удаления получателя рассылки (клиента)
    '''
    model = Recipient
    template_name = 'dispatcher/recipient_delete.html'
    success_url = reverse_lazy('dispatcher:recipients_list')