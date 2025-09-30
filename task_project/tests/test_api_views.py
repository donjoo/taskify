from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import CustomUser
from tasks.models import Task
from django.urls import reverse
from datetime import date

class TaskAPITest(APITestCase):

    def setUp(self):
        self.superadmin = CustomUser.objects.create_user(email="superadmin@example.com", password="pass123", role="superadmin")
        self.admin = CustomUser.objects.create_user(email="admin@example.com", password="pass123", role="admin")
        self.user = CustomUser.objects.create_user(email="user@example.com", password="pass123", role="user", admin=self.admin)

        self.task = Task.objects.create(
            title="Task 1",
            description="Task desc",
            assigned_admin=self.admin,
            assigned_to=self.user,
            due_date=date.today(),
            status="pending"
        )

        # JWT token simulation if using JWT Auth
        self.client.force_authenticate(user=self.user)

    def test_task_list_api(self):
        url = reverse('task_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_task_update_requires_report(self):
        url = reverse('task_update', kwargs={'id': self.task.id})
        data = {'status': 'completed', 'completion_report': '', 'worked_hours': ''}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_task_report_api_completed_only(self):
        self.task.status = "pending"
        self.task.save()
        url = reverse('task_report', kwargs={'id': self.task.id})
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Now mark as completed
        self.task.status = "completed"
        self.task.completion_report = "Finished task"
        self.task.worked_hours = 3
        self.task.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['completion_report'], "Finished task")
