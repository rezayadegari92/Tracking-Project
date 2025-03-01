# admin.py
from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type')
    list_filter = ('user_type',)

admin.site.register(CustomUser, CustomUserAdmin)