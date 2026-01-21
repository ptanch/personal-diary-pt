from django.test import TestCase
from django import forms
from django.contrib.auth import get_user_model

from users.forms import UserRegisterForm, LoginForm, UserProfileForm


User = get_user_model()


class UserFormsTestCase(TestCase):
    def test_register_form_valid_and_saves_user(self):
        """Проверяет валидность формы регистрации при корректных данных и сохранение пользователя"""
        form = UserRegisterForm(data={
            "email": "new@example.com",
            "password1": "StrongPass123!@#",
            "password2": "StrongPass123!@#",
        })
        self.assertTrue(form.is_valid(), form.errors.as_text())

        user = form.save()
        self.assertIsNotNone(user.pk)
        self.assertEqual(user.email, "new@example.com")

    def test_register_form_invalid_when_passwords_do_not_match(self):
        """Проверяет, что форма регистрации становится невалидной, если пароли не совпадают"""
        form = UserRegisterForm(data={
            "email": "new@example.com",
            "password1": "StrongPass123!@#",
            "password2": "DIFFERENTpass123!@#",
        })
        self.assertFalse(form.is_valid())
        # стандартная ошибка Django на password2
        self.assertIn("password2", form.errors)

    def test_register_form_invalid_when_email_already_exists(self):
        """Проверяет валидацию формы при попытке регистрации с существующим email"""
        User.objects.create_user(email="dup@example.com", password="StrongPass123!")
        form = UserRegisterForm(data={
            "email": "dup@example.com",
            "password1": "StrongPass123!@#",
            "password2": "StrongPass123!@#",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_register_form_applies_bootstrap_class(self):
        """Проверяет применение Bootstrap-классов к полям формы регистрации"""
        form = UserRegisterForm()
        # StyleFormMixin должен добавить form-control
        self.assertIn("form-control", form.fields["email"].widget.attrs.get("class", ""))

    def test_register_form_sets_password_placeholders(self):
        """Проверяет установку placeholder'ов для полей паролей в форме регистрации"""
        form = UserRegisterForm()
        self.assertEqual(form.fields["password1"].widget.attrs.get("placeholder"), "Password")
        self.assertEqual(form.fields["password2"].widget.attrs.get("placeholder"), "Repeat password")

    def test_login_form_has_bootstrap_attrs(self):
        """Проверяет наличие Bootstrap-классов и placeholder'ов в форме входа"""
        form = LoginForm()
        self.assertIn("form-control", form.fields["username"].widget.attrs.get("class", ""))
        self.assertEqual(form.fields["username"].widget.attrs.get("placeholder"), "name@example.com")

        self.assertIn("form-control", form.fields["password"].widget.attrs.get("class", ""))
        self.assertEqual(form.fields["password"].widget.attrs.get("placeholder"), "Password")

    def test_profile_form_date_widget_is_date_input(self):
        """Проверяет тип виджета для поля date_of_birth в форме профиля"""
        form = UserProfileForm()
        self.assertIsInstance(
            form.fields["date_of_birth"].widget,
            forms.DateInput
        )

    def test_profile_form_valid(self):
        """Проверка валидности формы профиля при корректных данных"""
        user = User.objects.create_user(email="u@example.com", password="StrongPass123!")
        form = UserProfileForm(
            data={
                "first_name": "Tanya",
                "last_name": "Tester",
                "phone": "+49123456789",
                "sex": "N",
                "date_of_birth": "1994-07-23",
            },
            instance=user,
        )
        self.assertTrue(form.is_valid(), form.errors.as_text())
