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
    
    subjects = Subject.objects.filter(teacher=request.user)
    
    if request.method == 'POST':
        try:
            # Get basic quiz info
            title = request.POST.get('title')
            subject_id = request.POST.get('subject')
            duration = request.POST.get('duration')
            description = request.POST.get('description', '')
            
            # Create quiz
            subject = get_object_or_404(Subject, id=subject_id, teacher=request.user)
            quiz = Quiz.objects.create(
                title=title,
                subject=subject,
                description=description,
                duration=duration,
                created_by=request.user
            )
            
            # Parse questions
            questions_data = {}
            for key, value in request.POST.items():
                if key.startswith('questions['):
                    # Parse question ID and field name
                    parts = key.split('[')
                    question_id = parts[1].rstrip(']')
                    field_name = parts[2].rstrip(']')
                    
                    if question_id not in questions_data:
                        questions_data[question_id] = {}
                    
                    if field_name == 'options':
                        if 'options' not in questions_data[question_id]:
                            questions_data[question_id]['options'] = []
                        questions_data[question_id]['options'].append(value)
                    else:
                        questions_data[question_id][field_name] = value
            
            # Create questions
            for idx, (q_id, q_data) in enumerate(sorted(questions_data.items()), start=1):
                question_text = q_data.get('text', '')
                question_type = q_data.get('type', 'multiple_choice')
                points = int(q_data.get('points', 1))
                
                if question_type == 'short_answer':
                    correct_answer = q_data.get('correct_answer', '')
                    options = []
                else:
                    correct_index = q_data.get('correct', '0')
                    options = q_data.get('options', [])
                    correct_answer = correct_index
                
                Question.objects.create(
                    quiz=quiz,
                    text=question_text,
                    question_type=question_type,
                    options=options,
                    correct_answer=correct_answer,
                    points=points,
                    order=idx
                )
            
            messages.success(request, f'Quiz "{quiz.title}" created successfully with {len(questions_data)} questions!')
            return redirect('teacher_dashboard')
            
        except Exception as e:
            messages.error(request, f'Error creating quiz: {str(e)}')
            return render(request, 'teachers/create_quiz.html', {'subjects': subjects})
    
    return render(request, 'teachers/create_quiz.html', {'subjects': subjects})
