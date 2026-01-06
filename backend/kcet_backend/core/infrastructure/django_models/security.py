from django.db import models

class UserRole(models.TextChoices):
    STUDENT = "STUDENT"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.STUDENT)

    def __str__(self):
        return f"{self.user.username} → {self.role}"

