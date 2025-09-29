from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.utils import role_check
from django.http import HttpResponseForbidden
from accounts.models import CustomUser
from tasks.models import Task   


@login_required
def superadmin_dashboard(request):
    if not role_check(request.user, ['superadmin']):
        return HttpResponseForbidden("Forbidden")
    

    
    users = CustomUser.objects.all()
    tasks = Task.objects.all()
    return render(request, 'admin_panel/superadmin_dashboard.html',{
        'users': users,
        'tasks': tasks
    })



