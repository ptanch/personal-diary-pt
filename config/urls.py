from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls", namespace="users")),
    path("diary/", include("diary.urls", namespace="diary")),
]
