from django import forms
from .models import CustomUser


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role','admin']

    def save(self,commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user