from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('subject/<int:subject_id>/', views.student_subject_detail, name='student_subject_detail'),
    path('magnify-learning/', views.magnify_learning, name='magnify_learning'),
    path('pdf-chat/<int:pdf_id>/', views.pdf_chat, name='pdf_chat'),
    path('ask-question/<int:pdf_id>/', views.ask_question, name='ask_question'),
    path('summarizer/', views.summarizer, name='summarizer'),
    path('generate-summary/', views.generate_summary, name='generate_summary'),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz/take/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quiz/submit/<int:quiz_id>/', views.submit_quiz, name='submit_quiz'),
]
