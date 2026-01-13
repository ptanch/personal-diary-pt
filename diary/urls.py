from django.urls import path
from .views import (
    DiaryListView,
    DiaryDetailView,
    DiaryCreateView,
    DiaryUpdateView,
    DiaryDeleteView,
)

app_name = "diary"

urlpatterns = [
    path("", DiaryListView.as_view(), name="diary_list"),
    path("create/", DiaryCreateView.as_view(), name="diary_create"),
    path("<int:pk>/", DiaryDetailView.as_view(), name="diary_detail"),
    path("<int:pk>/update/", DiaryUpdateView.as_view(), name="diary_update"),
    path("<int:pk>/delete/", DiaryDeleteView.as_view(), name="diary_delete"),
]
