# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('superadmin', 'Super Admin'),
        ('partner', 'Partner'),
        ('customer', 'Customer'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')

    # Add related_name to avoid clashes with default User model
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_groups",  # Unique related_name
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_permissions",  # Unique related_name
        related_query_name="customuser",
    )

    def __str__(self):
        return f"{self.username} - {self.get_user_type_display()}"