from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('subject/create/', views.create_subject, name='create_subject'),
    path('subject/<int:subject_id>/', views.subject_detail, name='teacher_subject_detail'),
    path('subject/<int:subject_id>/upload/', views.upload_pdf, name='upload_pdf'),
    path('quiz/create/', views.create_quiz, name='create_quiz'),
]
