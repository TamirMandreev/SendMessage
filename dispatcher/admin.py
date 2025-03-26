from django.contrib import admin

# Register your models here.

from dispatcher.models import Recipient, Message, Mailing, AttemptToMailing

@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'comment')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('theme', 'body',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('status', 'message',)


@admin.register(AttemptToMailing)
class AttemptToMailingAdmin(admin.ModelAdmin):
    list_display = ('date_time_of_attempt', 'status', 'mail_server_response', 'mailing', 'messages_count')