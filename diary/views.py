from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from diary.forms import DiaryForm
from diary.models import Diary


class DiaryCreateView(LoginRequiredMixin, CreateView):
    """Создание дневниковой записи"""

    model = Diary
    template_name = "diary/diary_form.html"
    form_class = DiaryForm
    success_url = reverse_lazy("diary:diary_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DiaryListView(LoginRequiredMixin, ListView):
    """Список дневниковых записей"""

    model = Diary
    template_name = "diary/diary_list.html"
    context_object_name = "entries"
    paginate_by = 10

    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user).order_by("-created_at")


class DiaryDetailView(LoginRequiredMixin, DetailView):
    """Просмотр конкретной дневниковой записи"""

    model = Diary
    template_name = "diary/diary_detail.html"
    context_object_name = "diary"

    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user)


class DiaryUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование дневниковой записи"""

    model = Diary
    form_class = DiaryForm
    template_name = "diary/diary_form.html"
    success_url = reverse_lazy("diary:diary_list")

    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user)


class DiaryDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление дневниковой записи"""

    model = Diary
    template_name = "diary/diary_confirm_delete.html"
    success_url = reverse_lazy("diary:diary_list")

    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user)
