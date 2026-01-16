from django.urls import path
from django.contrib.auth import views as auth_views

from users.views import UserCreateView, UserLoginView, UserProfileView

app_name = "users"

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="users:login"), name="logout"),
    path("profile/", UserProfileView.as_view(), name="profile")
]
