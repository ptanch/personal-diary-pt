from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from users.mixins import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")

        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "name@example.com"}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.fields["password1"].widget.attrs.setdefault("placeholder", "Password")
            self.fields["password2"].widget.attrs.setdefault("placeholder", "Repeat password")


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "name@example.com",
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Password",
        }),
    )
