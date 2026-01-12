from django.contrib import admin

from diary.models import Diary


@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "is_private", "created_at", "updated_at")
    list_filter = ("is_private", "created_at")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "updated_at")
