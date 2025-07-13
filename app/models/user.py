from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        USER = 'USER', 'User'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER
    )
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        # Automatically set superusers to have ADMIN role
        if self.is_superuser and self.role != self.Role.ADMIN:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)

    def is_admin(self):
        return self.role == self.Role.ADMIN

    def is_user(self):
        return self.role == self.Role.USER 