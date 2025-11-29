from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST
from teachers.models import Subject, PDFNote
from .models import ChatHistory
from .utils import get_answer_for_pdf
import json

@login_required
def student_dashboard(request):
    if not request.user.is_student():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    subjects = Subject.objects.all()
    return render(request, 'students/dashboard.html', {'subjects': subjects})

@login_required
def student_subject_detail(request, subject_id):
    if not request.user.is_student():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    subject = get_object_or_404(Subject, id=subject_id)
    notes = subject.notes.all()
    
    return render(request, 'students/subject_detail.html', {'subject': subject, 'notes': notes})

@login_required
def magnify_learning(request):
    if not request.user.is_student():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    subjects = Subject.objects.all().prefetch_related('notes')
    return render(request, 'students/magnify_learning.html', {'subjects': subjects})

@login_required
def pdf_chat(request, pdf_id):
    if not request.user.is_student():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    pdf_note = get_object_or_404(PDFNote, id=pdf_id)
    chat_history = ChatHistory.objects.filter(student=request.user, pdf_note=pdf_note)
    
    return render(request, 'students/pdf_chat.html', {
        'pdf_note': pdf_note,
        'chat_history': chat_history
    })

@login_required
@require_POST
def ask_question(request, pdf_id):
    if not request.user.is_student():
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        pdf_note = get_object_or_404(PDFNote, id=pdf_id)
        data = json.loads(request.body)
        question = data.get('question', '').strip()
        
        if not question:
            return JsonResponse({'error': 'Question is required'}, status=400)
        
        # Get previous chat history for context
        previous_chats = ChatHistory.objects.filter(
            student=request.user, 
            pdf_note=pdf_note
        ).order_by('-created_at')[:5]
        
        # Build chat history string
        history_text = ""
        for chat in reversed(previous_chats):
            history_text += f"Q: {chat.question}\nA: {chat.answer}\n\n"
        
        # Get PDF file path
        pdf_path = pdf_note.pdf_file.path
        
        # Get answer using the utility function
        answer = get_answer_for_pdf(pdf_path, question, history_text)
        
        # Save to chat history
        chat = ChatHistory.objects.create(
            student=request.user,
            pdf_note=pdf_note,
            question=question,
            answer=answer
        )
        
        return JsonResponse({
            'success': True,
            'answer': answer,
            'question': question,
            'timestamp': chat.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def quiz(request):
    if not request.user.is_student():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    from teachers.models import Quiz
    quizzes = Quiz.objects.filter(is_active=True).select_related('subject', 'pdf_note')
    return render(request, 'students/quiz.html', {'quizzes': quizzes})

@login_required
def take_quiz(request, quiz_id):
    if not request.user.is_student():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    from teachers.models import Quiz, QuizAttempt
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    questions = quiz.questions.all()
    
    # Check if already attempted
    existing_attempt = QuizAttempt.objects.filter(student=request.user, quiz=quiz, completed_at__isnull=False).first()
    
    return render(request, 'students/take_quiz.html', {
        'quiz': quiz,
        'questions': questions,
        'already_attempted': existing_attempt
    })

@login_required
@require_POST
def submit_quiz(request, quiz_id):
    if not request.user.is_student():
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    try:
        from teachers.models import Quiz, QuizAttempt, Question
        from django.utils import timezone
        
        quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
        data = json.loads(request.body)
        answers = data.get('answers', {})
        
        # Calculate score
        score = 0
        total_questions = quiz.questions.count()
        correct_answers = {}
        
        for question in quiz.questions.all():
            question_id = str(question.id)
            student_answer = answers.get(question_id)
            correct_answer = question.correct_answer
            
            if student_answer == correct_answer:
                score += 1
                correct_answers[question_id] = True
            else:
                correct_answers[question_id] = False
        
        # Save attempt
        attempt = QuizAttempt.objects.create(
            quiz=quiz,
            student=request.user,
            completed_at=timezone.now(),
            score=score,
            total_points=total_questions,
            answers=answers
        )
        
        percentage = (score / total_questions * 100) if total_questions > 0 else 0
        
        return JsonResponse({
            'success': True,
            'score': score,
            'total': total_questions,
            'percentage': round(percentage, 2),
            'correct_answers': correct_answers
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
