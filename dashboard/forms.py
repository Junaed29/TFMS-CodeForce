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
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'department', 'is_locked', 'password']
        widgets = {
             'username': forms.TextInput(attrs={'class': 'form-control'}),
             'first_name': forms.TextInput(attrs={'class': 'form-control'}),
             'last_name': forms.TextInput(attrs={'class': 'form-control'}),
             'email': forms.EmailInput(attrs={'class': 'form-control'}),
             'role': forms.Select(attrs={'class': 'form-select'}),
             'department': forms.Select(attrs={'class': 'form-select'}),
             'is_locked': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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
        fields = ['name', 'departments', 'description', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'departments': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class TaskForceMembershipForm(forms.ModelForm):
    class Meta:
        model = TaskForce
        fields = ['chairman', 'members']
        widgets = {
            'chairman': forms.Select(attrs={'class': 'form-select'}),
            'members': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        department = kwargs.pop('department', None)
        super().__init__(*args, **kwargs)
        if department:
            # Only show staff from the HOD's department for both Chairman and Members
            staff_qs = User.objects.filter(department=department, role__in=[User.Role.LECTURER, User.Role.DEAN, User.Role.HOD, User.Role.PSM])
            self.fields['members'].queryset = staff_qs
            self.fields['chairman'].queryset = staff_qs
