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
        ('ACTIVE', 'Active (Draft)'),
        ('SUBMITTED', 'Submitted for Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('INACTIVE', 'Inactive'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    departments = models.ManyToManyField(Department, related_name='task_forces')
    chart_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    
    chairman = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='chaired_task_forces')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='task_force_memberships', blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def is_fully_staffed(self):
        # Placeholder for complex logic (e.g. min 3 members)
        return self.members.count() >= 1

    def __str__(self):
        dept_names = ", ".join([d.name for d in self.departments.all()])
        return f"{self.name} ({dept_names})"
