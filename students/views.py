from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from teachers.models import Subject, PDFNote

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
    
    return render(request, 'students/magnify_learning.html')

@login_required
def quiz(request):
    if not request.user.is_student():
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    return render(request, 'students/quiz.html')
