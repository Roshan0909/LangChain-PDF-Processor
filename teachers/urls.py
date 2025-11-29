from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('subject/create/', views.create_subject, name='create_subject'),
    path('subject/<int:subject_id>/', views.subject_detail, name='teacher_subject_detail'),
    path('subject/<int:subject_id>/upload/', views.upload_pdf, name='upload_pdf'),
    path('quiz/create/', views.create_quiz, name='create_quiz'),
    path('quiz/generate/<int:pdf_id>/', views.generate_quiz, name='generate_quiz'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/toggle/', views.toggle_quiz_active, name='toggle_quiz_active'),
    path('quiz/analytics/', views.quiz_analytics, name='quiz_analytics'),
]
