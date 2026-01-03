from django.db import models
from django.conf import settings

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # HOD will be assigned via a OneToOne or ForeignKey in User/Profile, or here?
    # SRS says Admin assigns roles. If a User is HOD, they manage a Department.
    # Let's keep it simple: Department just has a name for now.
    
    def __str__(self):
        return self.name

class TaskForce(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    departments = models.ManyToManyField(Department, related_name='task_forces')
    chart_id = models.CharField(max_length=50, unique=True, blank=True, null=True) # For auto-gen ID
    
    # Memberships
    # We use a through model if we need to store extra data (e.g. role in taskforce)
    # For now, distinct Chairman and Members
    chairman = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='chaired_task_forces')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='task_force_memberships', blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        dept_names = ", ".join([d.name for d in self.departments.all()])
        return f"{self.name} ({dept_names})"
