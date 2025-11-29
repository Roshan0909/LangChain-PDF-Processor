from django.db import models
from authentication.models import User
import json

class Subject(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class PDFNote(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    pdf_file = models.FileField(upload_to='notes/%Y/%m/%d/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.subject.name}"
    
    class Meta:
        ordering = ['-created_at']

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes')
    pdf_note = models.ForeignKey(PDFNote, on_delete=models.CASCADE, related_name='quizzes', null=True)
    description = models.TextField(blank=True)
    duration = models.IntegerField(help_text="Duration in minutes", default=30)
    num_questions = models.IntegerField(default=10)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quizzes')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} - {self.subject.name}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Quizzes"

class Question(models.Model):
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
    ]
    
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    options = models.JSONField(default=list, blank=True)  # For multiple choice/true-false
    correct_answer = models.TextField()  # Index for MC/TF, text for short answer
    points = models.IntegerField(default=1)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.quiz.title} - Q{self.order}"
    
    class Meta:
        ordering = ['order']

class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    total_points = models.IntegerField(default=0)
    answers = models.JSONField(default=dict)  # Store student answers
    
    def __str__(self):
        return f"{self.student.username} - {self.quiz.title}"
    
    class Meta:
        ordering = ['-started_at']
