from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'SuperAdmin'),
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    admin = models.ForeignKey("self", null=True, blank=True, limit_choices_to={'role': 'admin'}, on_delete=models.SET_NULL, related_name="assigned_users")
    def is_superadmin(self):
        return self.role == 'superadmin'

    def is_admin(self):
        return self.role == 'admin'
