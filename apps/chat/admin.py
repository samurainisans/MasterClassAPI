from django.contrib import admin
from .models import Chat, Message

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('name', 'chat_status')
    search_fields = ('name',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat', 'user', 'type_msg', 'type_location', 'type_ack', 'content', 'time')
    search_fields = ('chat__name', 'user__username', 'type_msg', 'type_location', 'type_ack', 'content')
