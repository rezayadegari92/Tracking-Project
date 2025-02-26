from django.contrib import admin

# Register your models here.
from .models import CustomUser
class CustomUserAdmin(CustomUser):
    list_display = ('username', 'email', 'user_type')
    list_filter= ('user_type',)