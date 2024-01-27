from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["id",
                  "email","password","profile","fullName","phoneNumber","otp",
                  "is_active","is_staff",
                  "is_superuser","is_verified"]
    fieldsets = [
        (None, {"fields": ["email", "fullName",'phoneNumber', "password", 'profile','is_staff', 'is_active', 'is_superuser']})]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email",'fullName','phoneNumber','profile', "password1", "password2",'is_staff','is_active', 'is_superuser'],
            },
        ),
    ]
    search_fields = []
    ordering = []
    list_filter = []

@admin.register(Role)
class UserRole(admin.ModelAdmin):
    list_display = [
        'id','name','description',
    ]

admin.site.register(Avtar)