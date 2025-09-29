from django.urls import path
from . import views



urlpatterns = [
    path('superadmin/dashboard/', views.superadmin_dashboard, name='superadmin-dashboard'),
]