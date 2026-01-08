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
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        empty_label="Select Department",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'department']
        widgets = {
             'username': forms.TextInput(attrs={'class': 'form-control'}),
             'last_name': forms.TextInput(attrs={'class': 'form-control'}),
             'role': forms.Select(attrs={'class': 'form-select', 'id': 'id_role'}), # Added ID for JS targeting
        }
    
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        department = cleaned_data.get('department')
        
        # Roles requiring department
        dept_roles = [User.Role.HOD, User.Role.LECTURER]
        
        if role in dept_roles and not department:
            self.add_error('department', f"Department is required for {role}.")
            
        # Clear department for roles that don't need it
        if role not in dept_roles and department:
            cleaned_data['department'] = None
            
        return cleaned_data

class WorkloadSettingsForm(forms.ModelForm):
    class Meta:
        from university.models import WorkloadSettings
        model = WorkloadSettings
        fields = ['min_weightage', 'max_weightage']
        widgets = {
            'min_weightage': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_weightage': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        min_w = cleaned_data.get("min_weightage")
        max_w = cleaned_data.get("max_weightage")
        
        if min_w is not None and max_w is not None:
            if min_w < 0:
                self.add_error('min_weightage', "Min weightage cannot be negative.")
            if max_w > 30:
                self.add_error('max_weightage', "Max weightage cannot exceed 30.")
            if min_w >= max_w:
                raise forms.ValidationError("Max weightage must be greater than Min weightage.")
                
        return cleaned_data

class TaskForceForm(forms.ModelForm):
    class Meta:
        model = TaskForce
        fields = ['name', 'departments', 'description', 'status', 'weightage']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'departments': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'weightage': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from university.models import WorkloadSettings
        
        # Restrict Status choices for Admin (Create/Deactivate only)
        # Using the keys from TaskForce.STATUS_CHOICES: 'ACTIVE', 'INACTIVE'
        allowed_statuses = ['ACTIVE', 'INACTIVE']
        self.fields['status'].choices = [
            choice for choice in TaskForce.STATUS_CHOICES 
            if choice[0] in allowed_statuses
        ]

        settings = WorkloadSettings.objects.first()
        if settings:
            self.fields['weightage'].widget.attrs.update({
                'min': settings.min_weightage,
                'max': settings.max_weightage
            })
            self.fields['weightage'].help_text = f"Allowed range: {settings.min_weightage} - {settings.max_weightage}"
        else:
             self.fields['weightage'].widget.attrs.update({'min': 0, 'max': 30})
             self.fields['weightage'].help_text = "Allowed range: 0 - 30"
        
    def clean_weightage(self):
        weightage = self.cleaned_data.get('weightage')
        from university.models import WorkloadSettings
        # Get singleton or defaults (0, 30) if not exists yet
        settings = WorkloadSettings.objects.first() 
        min_val = settings.min_weightage if settings else 0
        max_val = settings.max_weightage if settings else 30
        
        if weightage is None:
             weightage = 5 # Default fallback
             
        if weightage < min_val or weightage > max_val:
            raise forms.ValidationError(f"Weightage must be between {min_val} and {max_val}.")
            
        return weightage

class TaskForceMembershipForm(forms.ModelForm):
    class Meta:
        model = TaskForce
        fields = ['members']
        widgets = {
            'members': forms.CheckboxSelectMultiple(),
        }
    
    def __init__(self, *args, **kwargs):
        department = kwargs.pop('department', None)
        super().__init__(*args, **kwargs)
        if department:
            # Only show staff from the HOD's department for Members
            staff_qs = User.objects.filter(
                department=department,
                role__in=[User.Role.LECTURER, User.Role.DEAN, User.Role.HOD, User.Role.PSM]
            )
            # Keep existing members selectable even if they belong to other departments.
            if self.instance.pk:
                staff_qs = staff_qs | self.instance.members.all()
            self.fields['members'].queryset = staff_qs.distinct()
