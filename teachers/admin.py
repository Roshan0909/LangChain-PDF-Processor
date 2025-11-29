from django.contrib import admin
from .models import Subject, PDFNote, Quiz, Question, QuizAttempt

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher', 'created_at']
    list_filter = ['teacher', 'created_at']
    search_fields = ['name', 'description']

@admin.register(PDFNote)
class PDFNoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'uploaded_by', 'created_at']
    list_filter = ['subject', 'uploaded_by', 'created_at']
    search_fields = ['title']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created_by', 'duration', 'is_active', 'created_at']
    list_filter = ['subject', 'created_by', 'is_active', 'created_at']
    search_fields = ['title', 'description']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'question_type', 'text', 'points', 'order']
    list_filter = ['quiz', 'question_type']
    search_fields = ['text']

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'student', 'started_at', 'completed_at', 'score', 'total_points']
    list_filter = ['quiz', 'student', 'started_at']
    search_fields = ['student__username', 'quiz__title']
