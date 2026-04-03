from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import TimeStampedModel


class Role(models.TextChoices):
    VIEWER = "viewer", "Viewer"
    ANALYST = "analyst", "Analyst"
    ADMIN = "admin", "Admin"


class User(AbstractUser, TimeStampedModel):
    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.VIEWER,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = Role.ADMIN
            self.is_staff = True
        super().save(*args, **kwargs) 

    def __str__(self):
        return self.email
    
    