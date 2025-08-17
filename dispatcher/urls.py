from django.urls import path

from dispatcher import views
from dispatcher.apps import DispatcherConfig
from dispatcher.views import AttemptToMailingListView

# Задать имя приложения в пространстве имен (namespace)
app_name = DispatcherConfig.name

urlpatterns = [
    path(
        "recipient/list/",
        views.RecipientListView.as_view(),
        name="recipients_list",
    ),
    path(
        "recipient/create/",
        views.RecipientCreateView.as_view(),
        name="recipient_create",
    ),
    path(
        "recipient/update/<int:pk>/",
        views.RecipientUpdateView.as_view(),
        name="recipient_update",
    ),
    path(
        "recipient/detail/<int:pk>/",
        views.RecipientDetailView.as_view(),
        name="recipient_detail",
    ),
    path(
        "recipient/delete/<int:pk>/",
        views.RecipientDeleteView.as_view(),
        name="recipient_delete",
    ),
    path(
        "message/create/",
        views.MessageCreateView.as_view(),
        name="message_create",
    ),
    path("message/list/", views.MessageListView.as_view(), name="messages_list"),
    path(
        "message/detail/<int:pk>/",
        views.MessageDetailView.as_view(),
        name="message_detail",
    ),
    path(
        "message/update/<int:pk>/",
        views.MessageUpdateView.as_view(),
        name="message_update",
    ),
    path(
        "message/delete/<int:pk>/",
        views.MessageDeleteView.as_view(),
        name="message_delete",
    ),
    path(
        "mailing/create/",
        views.MailingCreateView.as_view(),
        name="mailing_create",
    ),
    path("mailing/list/", views.MailingListView.as_view(), name="mailings_list"),
    path(
        "mailing/detail/<int:pk>/",
        views.MailingDetailView.as_view(),
        name="mailing_detail",
    ),
    path(
        "mailing/update/<int:pk>/",
        views.MailingUpdateView.as_view(),
        name="mailing_update",
    ),
    path(
        "mailing/delete/<int:pk>/",
        views.MailingDeleteView.as_view(),
        name="mailing_delete",
    ),
    path(
        "mailing/start/<int:pk>/",
        views.MailingStartView.as_view(),
        name="start_mailing",
    ),
    path("", views.Home.as_view(), name="home"),
    path(
        "attempt/list/",
        AttemptToMailingListView.as_view(),
        name="attempt_list",
    ),
]
