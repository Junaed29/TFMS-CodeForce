from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        HOD = "HOD", "Head of Department"
        PSM = "PSM", "Project Supervisor/Manager"
        DEAN = "DEAN", "Dean"
        LECTURER = "LECTURER", "Lecturer"

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.ADMIN)
    staff_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    department = models.ForeignKey('university.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='staff_members')
    
    # Account Locking Fields
    failed_attempts = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk and self.is_superuser:
            self.role = self.Role.ADMIN
        
        # Auto-generate Staff ID if not set
        if not self.staff_id and self.role != self.Role.ADMIN: # Admins might not need staff ID? Or yes? Use cases say "Staff ID".
             # Simple auto-increment logic or random?
             # Let's do simple increment: STF-{last_id + 1}
             last_user = User.objects.filter(staff_id__startswith='STF').order_by('staff_id').last()
             if last_user:
                 try:
                     last_id = int(last_user.staff_id.split('-')[1])
                     self.staff_id = f"STF-{last_id + 1:04d}"
                 except (IndexError, ValueError):
                     self.staff_id = "STF-0001"
             else:
                 self.staff_id = "STF-0001"
        
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class AuditLog(models.Model):
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=50)  # e.g. "LOGIN", "CREATE", "APPROVE"
    target_model = models.CharField(max_length=50, blank=True, null=True)
    target_id = models.CharField(max_length=50, blank=True, null=True)
    details = models.TextField(blank=True, null=True) # JSON or text justification
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.timestamp} - {self.actor} - {self.action}"
