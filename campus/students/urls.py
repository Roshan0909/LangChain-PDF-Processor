from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('subject/<int:subject_id>/', views.student_subject_detail, name='student_subject_detail'),
    path('magnify-learning/', views.magnify_learning, name='magnify_learning'),
    path('pdf-chat/<int:pdf_id>/', views.pdf_chat, name='pdf_chat'),
    path('ask-question/<int:pdf_id>/', views.ask_question, name='ask_question'),
    path('upload-and-chat/', views.upload_and_chat, name='upload_and_chat'),
    path('summarizer/', views.summarizer, name='summarizer'),
    path('generate-summary/', views.generate_summary, name='generate_summary'),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz/take/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quiz/submit/<int:quiz_id>/', views.submit_quiz, name='submit_quiz'),
    path('quiz/report/<int:attempt_id>/', views.quiz_report, name='quiz_report'),
    path('quiz/proctoring/<int:attempt_id>/', views.save_proctoring_snapshot, name='save_proctoring_snapshot'),
    path('chat/', views.student_chat, name='student_chat'),
    path('chat/<int:user_id>/', views.student_chat_with, name='student_chat_with'),
    path('knowledge-bot/', views.knowledge_bot, name='knowledge_bot'),
    path('knowledge-bot/ask/', views.knowledge_bot_ask, name='knowledge_bot_ask'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('practice-quiz/', views.practice_quiz, name='practice_quiz'),
    path('practice-quiz/generate/', views.generate_practice_quiz, name='generate_practice_quiz'),
    path('practice-quiz/take/<int:quiz_id>/', views.take_practice_quiz, name='take_practice_quiz'),
    path('practice-quiz/submit/<int:quiz_id>/', views.submit_practice_quiz, name='submit_practice_quiz'),
    path('practice-quiz/history/', views.practice_quiz_history, name='practice_quiz_history'),
]
