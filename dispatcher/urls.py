from django.urls import path

from dispatcher import views
from dispatcher.apps import DispatcherConfig

# Задать имя приложения в пространстве имен (namespace)
app_name = DispatcherConfig.name

urlpatterns = [
    path('', views.RecipientListView.as_view(), name='recipients_list'),
    path('recipient/create/', views.RecipientCreateView.as_view(), name='recipient_create'),
    path('recipient/update/<int:pk>/', views.RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipient/detail/<int:pk>/', views.RecipientDetailView.as_view(), name='recipient_detail'),
    path('recipient/delete/<int:pk>/', views.RecipientDeleteView.as_view(), name='recipient_delete'),
    path('message/create/', views.MessageCreateView.as_view(), name='message_create'),
    path('message/list/', views.MessageListView.as_view(), name='messages_list'),
    path('message/detail/<int:pk>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('message/update/<int:pk>/', views.MessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<int:pk>/', views.MessageDeleteView.as_view(), name='message_delete'),
]