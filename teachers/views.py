from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def teacher_dashboard(request):
    if not request.user.is_teacher():
        return HttpResponseForbidden("You don't have permission to access this page.")
    return render(request, 'teachers/dashboard.html')
