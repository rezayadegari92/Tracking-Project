from django.db import models

# Create your models here.
from  django.contrib.auth.models import  AbstractUser, Group, Permission


class CustomUser(AbstractUser):
    USER_TYPES =(
        ('superadmin', 'Super Admin'),
        ('partner', 'Partner'),
        ('customer', 'Customer'),

    )

    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    def __str__(self):
        return f"{self.username} - {self.get_user_type_display()}"


