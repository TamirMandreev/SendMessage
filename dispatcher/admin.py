from django.contrib import admin

# Register your models here.

from dispatcher.models import Recipient, Message, Mailing

@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'comment')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('theme', 'body',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('status', 'message',)