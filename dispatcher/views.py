from django.shortcuts import render
from django.views.generic import ListView, CreateView

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

# class RecipientCreateView(CreateView):
#     '''
#     Представление для создания получателей рассылки (клиентов)
#     '''
#     model = Recipient
#     form_class = RecipientForm