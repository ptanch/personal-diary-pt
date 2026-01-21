from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
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
        response = super().form_valid(form)
        messages.success(self.request, "Запись создана ✅")
        return response


class DiaryListView(LoginRequiredMixin, ListView):
    """Список дневниковых записей"""

    model = Diary
    template_name = "diary/diary_list.html"
    context_object_name = "entries"
    paginate_by = 9

    def get_queryset(self):
        qs = Diary.objects.filter(user=self.request.user).order_by("-created_at")

        q = (self.request.GET.get("q") or "").strip()
        if q:
            qs = qs.filter(
                Q(title__icontains=q) | Q(note__icontains=q)
            )

        return qs

    def get_context_data(self, **kwargs):
        """Метод для поисковой формы - отображает текущий поисковый запрос в поле ввода"""

        context = super().get_context_data(**kwargs)
        context["q"] = (self.request.GET.get("q") or "").strip()
        return context


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

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Запись обновлена ✅")
        return response


class DiaryDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление дневниковой записи"""

    model = Diary
    template_name = "diary/diary_confirm_delete.html"
    success_url = reverse_lazy("diary:diary_list")

    def get_queryset(self):
        return Diary.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, "Запись удалена 🗑️")
        return super().delete(request, *args, **kwargs)
