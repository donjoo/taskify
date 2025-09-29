from .models import Task
from .serializers import TaskSerializer, TaskStatusUpdateSerializer
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated




class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(assigned_to = self.request.user)
    

    