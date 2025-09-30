from django.urls import path
from . import views



urlpatterns = [

    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'),

    path('superadmin/dashboard/', views.superadmin_dashboard, name='superadmin_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # User CRUD (SuperAdmin only)
    path("users/create/", views.user_create, name="user_create"),
    path("users/<int:pk>/update/", views.user_update, name="user_update"),
    path("users/<int:pk>/delete/", views.user_delete, name="user_delete"),


    # Task CRUD (Admin + SuperAdmin)
    path("tasks/create/", views.task_create, name="task_create"),
    path("tasks/<int:pk>/update/", views.task_update, name="task_update"),
    path("tasks/<int:pk>/delete/", views.task_delete, name="task_delete"),


]