from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff", "current_counterparty")
    list_editable = ['current_counterparty']


admin.site.register(User, CustomUserAdmin)
