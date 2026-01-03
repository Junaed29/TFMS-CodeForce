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

    def save(self, *args, **kwargs):
        if not self.pk and self.is_superuser:
            self.role = self.Role.ADMIN
        return super().save(*args, **kwargs)
