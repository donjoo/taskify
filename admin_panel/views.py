from django.shortcuts import render , redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.utils import role_check
from django.http import HttpResponseForbidden
from accounts.models import CustomUser
from tasks.models import Task   
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from accounts.forms import UserForm
from tasks.forms import TaskForm


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
def user_create(request):
    if request.user.role != "superadmin":
        return redirect('login')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('superadmin_dashboard')
    else:
        form = UserForm()
    return render(request, 'admin_panel/user_form.html', {'form': form})   

@login_required
def user_update(request,pk):
    if request.user.role != "superadmin":
        return redirect('login')
    user = get_object_or_404(CustomUser, pk=pk)
    form = UserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('superadmin_dashboard')
    return render(request, 'admin_panel/user_form.html', {'form': form})


@login_required
def user_delete(request, pk):
    if request.user.role != "superadmin":
        return redirect('login')
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('superadmin_dashboard')
    return render(request, 'admin_panel/user_confirm_delete.html', {'user': user})



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






# <<<<<<<<<<<<<<<<<<---------------------- TASK VIEWS ---------------------------------->>>>>>>>>>>>>>>>>>>




@login_required
def task_create(request):
    if not role_check(request.user, ['admin','superadmin']):
        return redirect('login')
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin_dashboard" if request.user.role == "admin" else "superadmin_dashboard") 
        else:
            form = TaskForm()
    return render(request, 'admin_panel/task_form.html', {'form': form})




@login_required
def task_update(request,pk):
    if not role_check(request.user, ['admin','superadmin']):
        return redirect('login')
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        return redirect("admin_dashboard" if request.user.role == "admin" else "superadmin_dashboard")
    return render(request, 'admin_panel/task_form.html', {'form': form})




@login_required
def task_delete(request, pk):
    if not role_check(request.user, ['admin','superadmin']):
        return redirect('login')
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect("admin_dashboard" if request.user.role == "admin" else "superadmin_dashboard")
    return render(request, 'admin_panel/task_confirm_delete.html', {'task': task})