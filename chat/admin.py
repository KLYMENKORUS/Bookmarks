from django.contrib import admin
from .models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    # list_display = ['type']
    autocomplete_fields = ['members']
    search_fields = ('members',)
    actions = ['fix_last_messages']

    def fix_last_messages(self, request, queryset):
        for chat in queryset.all():
            chat.last_message = chat.message_set.all().order_by('-pub_date').first()
            chat.save(update_fields=['last_message'])

    fix_last_messages.short_description = 'Fix last messages'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    autocomplete_fields = ['chat', 'author']
    list_display = ['chat', 'author', 'pub_date', 'is_read']
