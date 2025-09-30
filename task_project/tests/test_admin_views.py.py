from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser
from tasks.models import Task
from datetime import date

class AdminPanelViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
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

    def test_superadmin_dashboard_access(self):
        self.client.login(email="superadmin@example.com", password="pass123")
        response = self.client.get(reverse("superadmin_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tasks")
        self.assertContains(response, "Users")

    def test_admin_dashboard_access(self):
        self.client.login(email="admin@example.com", password="pass123")
        response = self.client.get(reverse("admin_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.email)
        self.assertContains(response, self.task.title)

    def test_admin_user_detail_view(self):
        self.client.login(email="admin@example.com", password="pass123")
        response = self.client.get(reverse("admin_user_detail", args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.title)

    def test_superadmin_user_detail_view(self):
        self.client.login(email="superadmin@example.com", password="pass123")
        response = self.client.get(reverse("superadmin_user_detail", args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.title)
