from .models import Task
from .serializers import TaskSerializer, TaskStatusUpdateSerializer
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

def _user_role(user):
    """Helper function to get user role"""
    return getattr(user, 'role', None)


class IsAdminOrSuperAdmin(permissions.BasePermission):
    """
    Custom permission to allow only users with role 'admin' or 'superadmin'.
    """
    def has_permission(self, request, view):
        return _user_role(request.user) in ('admin', 'superadmin') 



class TaskListView(generics.ListAPIView):
    """
    API endpoint to list all the tasks assigned to the loggedd-in user.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assigned_to = self.request.user)
    

class TaskUpdateView(generics.UpdateAPIView):
    """
    API endpoint for users to update the status of their assigned tasks.
    User can mark a task as completed and must provide a completion report and worked hours.
    serialier checks wheather completion report and worked hours are provided.
    """
    queryset = Task.objects.all()
    serializer_class = TaskStatusUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'id'


    def get_object(self):
        obj = get_object_or_404(Task, id=self.kwargs.get('id'))
        if obj.assigned_to != self.request.user:
           self.permission_denied(self.request, message="You do not have persmission to edit this task.")
        return obj
    


class TaskReportView(generics.RetrieveAPIView):
    """
    Api endpoint for admins and superadmin to view task completion report
    ONly for tast with status "completed"


    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]
    lookup_url_kwarg = 'id'


    def get_object(self):
        """
        
        Retrieve task obj by id and checks if its status is "completed"
        """
        obj = get_object_or_404(Task, id=self.kwargs.get('id'))
        if obj.status != 'completed':
            self.permission_denied(self.request, message="Report only savailable for completed tasks.")
        return obj
    

    def get(self, request, *args, **kwargs):
        """
        
        return the completion report and worked hours  
        """
        task = self.get_object()
        data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,    
            'completion_report': task.completion_report,
            'worked_hours': task.worked_hours,  
            'completed_at': task.updated_at,    
        }
        return Response(data, status=status.HTTP_200_OK)   
    


