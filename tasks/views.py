from .models import Task
from .serializers import TaskSerializer, TaskStatusUpdateSerializer
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404



def _user_role(user):
    return getattr(user, 'role', None)


class IsAdminOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return _user_role(request.user) in ('admin', 'superadmin') 



class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assigned_to = self.request.user)
    

class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskStatusUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'id'


    def get_object(self):
        obj = get_object_or_404(Task, id=self.kwargs.get('id'))
        if obj.assigned_to != self.request.user:
           self.permission_denied(self.request, message="You do not have persmission to edit this task.")
        return obj
    
