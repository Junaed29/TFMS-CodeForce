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
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted for Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('INACTIVE', 'Inactive'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True) # Feedback from PSM
    departments = models.ManyToManyField(Department, related_name='task_forces')
    chart_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    weightage = models.IntegerField(default=5)
    
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

class WorkloadSettings(models.Model):
    min_weightage = models.IntegerField(default=0)
    max_weightage = models.IntegerField(default=30)

    def save(self, *args, **kwargs):
        if not self.pk and WorkloadSettings.objects.exists():
            # If it's a new instance but one already exists, prevent it (though UI should handle this)
            # We can also just return the existing unique instance, but raising an error is safer for now.
             import django.core.exceptions
             raise django.core.exceptions.ValidationError('There can be only one WorkloadSettings instance')
             
        if self.min_weightage >= self.max_weightage:
             import django.core.exceptions
             raise django.core.exceptions.ValidationError('Max weightage must be greater than Min weightage')
             
        return super().save(*args, **kwargs)

    def __str__(self):
        return "Workload Configuration"
        
    class Meta:
        verbose_name_plural = "Workload Settings"
