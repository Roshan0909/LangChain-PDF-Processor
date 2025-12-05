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

class PracticeQuiz(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='practice_quizzes')
    title = models.CharField(max_length=200)
    pdf_note = models.ForeignKey(PDFNote, on_delete=models.SET_NULL, null=True, blank=True, related_name='practice_quizzes')
    uploaded_file = models.FileField(upload_to='practice_files/%Y/%m/%d/', null=True, blank=True)
    topic = models.CharField(max_length=200, blank=True)
    difficulty = models.CharField(max_length=20, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='medium')
    num_questions = models.IntegerField(default=5)
    questions_data = models.JSONField(default=list)  # Store generated questions
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.title}"
    
    def get_file_name(self):
        if self.pdf_note:
            return self.pdf_note.title
        elif self.uploaded_file:
            return self.uploaded_file.name.split('/')[-1]
        return "No file"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Practice Quizzes"

class PracticeQuizAttempt(models.Model):
    practice_quiz = models.ForeignKey(PracticeQuiz, on_delete=models.CASCADE, related_name='attempts')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='practice_attempts')
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    answers = models.JSONField(default=dict)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.practice_quiz.title} - {self.score}/{self.total_questions}"
    
    class Meta:
        ordering = ['-completed_at']

class StudentProfile(models.Model):
    """Extended student profile with essential details"""
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=200, blank=True)
    class_name = models.CharField(max_length=100, blank=True)
    roll_number = models.CharField(max_length=50, blank=True)
    registration_number = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email_id = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.username} - Profile"
    
    class Meta:
        verbose_name_plural = "Student Profiles"
