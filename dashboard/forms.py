from django import forms
from django.contrib.auth import get_user_model
from university.models import TaskForce, Department

User = get_user_model()

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class StaffForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'department', 'password']
        widgets = {
             'username': forms.TextInput(attrs={'class': 'form-control'}),
             'first_name': forms.TextInput(attrs={'class': 'form-control'}),
             'last_name': forms.TextInput(attrs={'class': 'form-control'}),
             'email': forms.EmailInput(attrs={'class': 'form-control'}),
             'role': forms.Select(attrs={'class': 'form-select'}),
             'department': forms.Select(attrs={'class': 'form-select'}),
             'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

class TaskForceForm(forms.ModelForm):
    class Meta:
        model = TaskForce
        fields = ['name', 'departments', 'description', 'chairman', 'members', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'departments': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'chairman': forms.Select(attrs={'class': 'form-select'}),
            'members': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 10}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
