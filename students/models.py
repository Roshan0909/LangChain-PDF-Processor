from django.db import models
from authentication.models import User
from teachers.models import PDFNote

class ChatHistory(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_histories')
    pdf_note = models.ForeignKey(PDFNote, on_delete=models.CASCADE, related_name='chat_histories')
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.pdf_note.title} - {self.created_at}"
    
    class Meta:
        ordering = ['created_at']
        verbose_name_plural = "Chat Histories"

class KnowledgeBotHistory(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='knowledge_bot_histories')
    question = models.TextField()
    answer = models.TextField()
    sources = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.created_at}"
    
    class Meta:
        ordering = ['created_at']
        verbose_name_plural = "Knowledge Bot Histories"
