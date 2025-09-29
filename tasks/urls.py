from django.urls import path
from .views import TaskListView, TaskUpdateView, TaskReportView



urlpatterns = [
    path('tasks/', TaskListView.as_view(),name='task-list'),
    path('tasks/<init:id>/', TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<init:id>/report/', TaskReportView.as_view(), name='task-report'),

    
]