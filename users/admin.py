from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from users.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    ordering = ("email",)
    list_display = ("id", "email", "first_name", "last_name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "sex")
    search_fields = ("email", "first_name", "last_name", "phone")
