from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def student_dashboard(request):
    if not request.user.is_student():
        return HttpResponseForbidden("You don't have permission to access this page.")
    return render(request, 'students/dashboard.html')
