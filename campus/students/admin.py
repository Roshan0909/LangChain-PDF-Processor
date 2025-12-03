from django.contrib import admin
from .models import ChatHistory, KnowledgeBotHistory

@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ['student', 'pdf_note', 'question', 'created_at']
    list_filter = ['student', 'pdf_note', 'created_at']
    search_fields = ['question', 'answer', 'student__username']
    readonly_fields = ['created_at']

@admin.register(KnowledgeBotHistory)
class KnowledgeBotHistoryAdmin(admin.ModelAdmin):
    list_display = ['student', 'question', 'created_at']
    list_filter = ['student', 'created_at']
    search_fields = ['question', 'answer', 'student__username']
    readonly_fields = ['created_at', 'sources']
