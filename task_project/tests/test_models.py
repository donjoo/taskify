from django.test import TestCase
from accounts.models import CustomUser
from tasks.models import Task
from datetime import date

class TaskModelTest(TestCase):

    def setUp(self):
        self.superadmin = CustomUser.objects.create_user(email="superadmin@example.com", password="pass123", role="superadmin")
        self.admin = CustomUser.objects.create_user(email="admin@example.com", password="pass123", role="admin")
        self.user = CustomUser.objects.create_user(email="user@example.com", password="pass123", role="user", admin=self.admin)
        
        self.task = Task.objects.create(
            title="Test Task",
            description="Task desc",
            assigned_admin=self.admin,
            assigned_to=self.user,
            due_date=date.today(),
            status="pending"
        )

    def test_task_str(self):
        self.assertEqual(str(self.task), "Test Task (pending)")

    def test_task_completion_requires_report(self):
        self.task.status = "completed"
        self.task.completion_report = None
        self.task.worked_hours = None
        with self.assertRaises(ValueError):
            if self.task.status == "completed" and (not self.task.completion_report or not self.task.worked_hours):
                raise ValueError("Completion report and worked hours required")
