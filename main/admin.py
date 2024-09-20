from django.contrib import admin

from main.models import Client, Message, Mailing, MailingLog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    list_filter = ('email',)
    verbose_name = 'Клиенты'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_filter = ('title',)
    verbose_name = 'Сообщения'


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'start_datetime')
    list_filter = ('start_datetime', 'message', 'status')
    verbose_name = 'Рассылки'


@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'mailing', 'status')
    list_filter = ('status',)
    verbose_name = 'Попытки отправки сообщений'
