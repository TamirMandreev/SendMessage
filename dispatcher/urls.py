from django.urls import path

from dispatcher import views
from dispatcher.apps import DispatcherConfig

# Задать имя приложения в пространстве имен (namespace)
app_name = DispatcherConfig.name

urlpatterns = [
    path('', views.RecipientListView.as_view(), name='recipients_list'),
]