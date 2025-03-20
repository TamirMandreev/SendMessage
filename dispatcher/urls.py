from django.urls import path

from dispatcher import views
from dispatcher.apps import DispatcherConfig

# Задать имя приложения в пространстве имен (namespace)
app_name = DispatcherConfig.name

urlpatterns = [
    path('', views.RecipientListView.as_view(), name='recipients_list'),
    path('recipient/create/', views.RecipientCreateView.as_view(), name='recipient_create'),
    path('recipient/update/<int:pk>/', views.RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipient/delete/<int:pk>/', views.RecipientDeleteView.as_view(), name='recipient_delete'),
]