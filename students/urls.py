from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('subject/<int:subject_id>/', views.student_subject_detail, name='student_subject_detail'),
    path('magnify-learning/', views.magnify_learning, name='magnify_learning'),
    path('quiz/', views.quiz, name='quiz'),
]
