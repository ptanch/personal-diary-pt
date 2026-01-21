from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import LoginForm, UserRegisterForm, UserProfileForm
from .models import User


class UserCreateView(CreateView):
    """Создание учетной записи пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("diary:diary_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Аккаунт создан! Добро пожаловать 👋")
        return response


class UserLoginView(LoginView):
    """Вход в учетную запись пользователя"""
    form_class = LoginForm
    template_name = "users/login.html"


class UserProfileView(LoginRequiredMixin, UpdateView):
    """Просмотр профиля пользователя"""
    model = User
    form_class = UserProfileForm
    template_name = "users/profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        """Пользователь может редактировать только себя"""
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Профиль обновлён ✅")
        return response
