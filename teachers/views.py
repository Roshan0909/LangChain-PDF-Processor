from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages
from .models import Subject, PDFNote, Quiz, Question
from .forms import SubjectForm, PDFNoteForm
import json

@login_required
def teacher_dashboard(request):
    if not request.user.is_teacher():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    subjects = Subject.objects.filter(teacher=request.user)
    quizzes = Quiz.objects.filter(created_by=request.user).order_by('-created_at')[:10]
    return render(request, 'teachers/dashboard.html', {'subjects': subjects, 'quizzes': quizzes})

@login_required
def create_subject(request):
    if not request.user.is_teacher():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.teacher = request.user
            subject.save()
            messages.success(request, f'Subject "{subject.name}" created successfully!')
            return redirect('teacher_dashboard')
    else:
        form = SubjectForm()
    
    return render(request, 'teachers/create_subject.html', {'form': form})

@login_required
def subject_detail(request, subject_id):
    if not request.user.is_teacher():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    subject = get_object_or_404(Subject, id=subject_id, teacher=request.user)
    notes = subject.notes.all()
    
    return render(request, 'teachers/subject_detail.html', {'subject': subject, 'notes': notes})

@login_required
def upload_pdf(request, subject_id):
    if not request.user.is_teacher():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    subject = get_object_or_404(Subject, id=subject_id, teacher=request.user)
    
    if request.method == 'POST':
        form = PDFNoteForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_note = form.save(commit=False)
            pdf_note.subject = subject
            pdf_note.uploaded_by = request.user
            pdf_note.save()
            messages.success(request, f'PDF "{pdf_note.title}" uploaded successfully!')
            return redirect('teacher_subject_detail', subject_id=subject.id)
    else:
        form = PDFNoteForm()
    
    return render(request, 'teachers/upload_pdf.html', {'form': form, 'subject': subject})

@login_required
def create_quiz(request):
    if not request.user.is_teacher():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    subjects = Subject.objects.filter(teacher=request.user).prefetch_related('notes')
    return render(request, 'teachers/create_quiz.html', {'subjects': subjects})

@login_required
def generate_quiz(request, pdf_id):
    if not request.user.is_teacher():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    pdf_note = get_object_or_404(PDFNote, id=pdf_id)
    
    if request.method == 'POST':
        try:
            from .quiz_generator import generate_quiz_from_pdf
            
            num_questions = int(request.POST.get('num_questions', 10))
            duration = int(request.POST.get('duration', 30))
            
            # Generate questions from PDF
            questions_data, error = generate_quiz_from_pdf(pdf_note.pdf_file.path, num_questions)
            
            if error:
                messages.error(request, error)
                return redirect('create_quiz')
            
            # Create quiz
            quiz = Quiz.objects.create(
                title=f"Quiz: {pdf_note.title}",
                subject=pdf_note.subject,
                pdf_note=pdf_note,
                description=f"Auto-generated quiz from {pdf_note.title}",
                duration=duration,
                num_questions=num_questions,
                created_by=request.user,
                is_active=True
            )
            
            # Create questions
            for idx, q_data in enumerate(questions_data, start=1):
                Question.objects.create(
                    quiz=quiz,
                    text=q_data['question'],
                    question_type='multiple_choice',
                    options=q_data['options'],
                    correct_answer=str(q_data['correct_answer']),
                    points=1,
                    order=idx
                )
            
            messages.success(request, f'Quiz "{quiz.title}" created successfully with {len(questions_data)} questions!')
            return redirect('quiz_analytics')
            
        except Exception as e:
            messages.error(request, f'Error generating quiz: {str(e)}')
            return redirect('create_quiz')
    
    return render(request, 'teachers/generate_quiz.html', {
        'pdf_note': pdf_note,
        'subject': pdf_note.subject
    })

@login_required
def quiz_analytics(request):
    if not request.user.is_teacher():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    quizzes = Quiz.objects.filter(created_by=request.user).prefetch_related('attempts', 'questions')
    
    # Calculate statistics for each quiz
    quiz_stats = []
    for quiz in quizzes:
        attempts = quiz.attempts.filter(completed_at__isnull=False)
        total_attempts = attempts.count()
        
        if total_attempts > 0:
            avg_score = sum(a.score for a in attempts) / total_attempts
            avg_percentage = (avg_score / quiz.questions.count()) * 100 if quiz.questions.count() > 0 else 0
        else:
            avg_score = 0
            avg_percentage = 0
        
        quiz_stats.append({
            'quiz': quiz,
            'total_attempts': total_attempts,
            'avg_score': round(avg_score, 2),
            'avg_percentage': round(avg_percentage, 2),
            'total_questions': quiz.questions.count()
        })
    
    return render(request, 'teachers/quiz_analytics.html', {'quiz_stats': quiz_stats})
