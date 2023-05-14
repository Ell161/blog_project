from django.contrib import admin
from .models import *


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'nickname', 'email', 'is_active', 'is_staff')
