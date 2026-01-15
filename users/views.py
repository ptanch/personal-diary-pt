from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import LoginForm, UserRegisterForm
from .models import User


class UserCreateView(CreateView):
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
    form_class = LoginForm
    template_name = "users/login.html"
