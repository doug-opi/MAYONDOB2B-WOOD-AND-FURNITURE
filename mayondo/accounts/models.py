from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('superadmin', 'Super Admin'),
        ('manager', 'Manager'),
        ('attendant', 'Attendant'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='attendant')
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    # Role check helpers
    def is_manager(self):
        return self.role == 'manager'

    def is_attendant(self):
        return self.role == 'attendant'

    def is_superadmin(self):
        return self.role == 'superadmin'
