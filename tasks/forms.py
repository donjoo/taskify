from django import forms
from .models import Task
from accounts.models import CustomUser


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", 'assigned_admin', "assigned_to", "due_date", "status"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),  # HTML5 date picker
        }



class TaskFormForAdmin(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date', 'status']
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),  # HTML5 date picker
        }

    def __init__(self, *args, **kwargs):
        admin = kwargs.pop('admin_user', None)
        super().__init__(*args, **kwargs)
        if admin:
            self.fields['assigned_to'].queryset = CustomUser.objects.filter(admin=admin)
