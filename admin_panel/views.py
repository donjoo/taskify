from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from accounts.utils import role_check
from django.http import HttpResponseForbidden
from accounts.models import CustomUser
from tasks.models import Task   
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages


# admin authenticate
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('superadmin_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'admin_panel/login.html', {'error': 'Invalid credentials'})
    return render(request, 'admin_panel/login.html')



def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def superadmin_dashboard(request):
    """# Superadmin dashboard view
    """
    if not role_check(request.user, ['superadmin']):
        return HttpResponseForbidden("Forbidden")
    

    
    users = CustomUser.objects.all()
    tasks = Task.objects.all()
    return render(request, 'admin_panel/superadmin_dashboard.html',{
        'users': users,
        'tasks': tasks
    })


@login_required
def admin_dashboard(request):
    if not role_check(request.user, ['admin','superadmin']):
        return HttpResponseForbidden("Forbidden")
    
    managed_users = CustomUser.objects.filter(role = 'user', )
    tasks = Task.objects.filter(assigned_to__in=managed_users)
    
    return render(request, 'admin_panel/admin_dashboard.html',{
        'users': managed_users,
        'tasks': tasks
    })



