from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages


User = get_user_model()


class UsersViewsTestCase(TestCase):
    """Тесты для контроллеров UserView"""
    def setUp(self):
        self.password = "StrongPass123!"
        self.user = User.objects.create_user(email="u1@example.com", password=self.password)

    def test_register_get_page_ok(self):
        """Проверяет, что страница регистрации доступна (GET-запрос)"""
        url = reverse("users:register")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "users/register.html")

    def test_register_creates_user_and_logs_in(self):
        """
        Проверяет процесс регистрации нового пользователя:
        - создание учётной записи;
        - автоматический вход после регистрации;
        - редирект на главную страницу дневника;
        - наличие сообщения об успешной регистрации
        """
        url = reverse("users:register")
        data = {
            "email": "new@example.com",
            "password1": "AnotherStrongPass123!",
            "password2": "AnotherStrongPass123!",
        }
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp["Location"], reverse("diary:diary_list"))

        # пользователь создан
        self.assertTrue(User.objects.filter(email="new@example.com").exists())

        # пользователь залогинен (проверка через доступ к защищенной странице профиля)
        profile_url = reverse("users:profile")
        resp2 = self.client.get(profile_url)
        self.assertEqual(resp2.status_code, 200)

        # сообщение о регистрации
        msgs = [m.message for m in get_messages(resp.wsgi_request)]
        self.assertIn("Аккаунт создан! Добро пожаловать 👋", msgs)

    def test_login_get_page_ok(self):
        """Проверяет, что страница входа доступна (GET-запрос)"""
        url = reverse("users:login")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "users/login.html")

    def test_login_success_redirects_to_login_redirect_url(self):
        """
        По умолчанию LoginView после успешного входа редиректит на LOGIN_REDIRECT_URL,
        если нет ?next=
        """
        url = reverse("users:login")
        data = {"username": self.user.email, "password": self.password}
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp["Location"], reverse("diary:diary_list"))

    def test_login_respects_next_parameter(self):
        """Проверяет обработку параметра next при входе"""
        url = reverse("users:login")
        next_url = reverse("users:profile")
        data = {"username": self.user.email, "password": self.password}

        resp = self.client.post(f"{url}?next={next_url}", data=data)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp["Location"], next_url)

    def test_profile_requires_login(self):
        """Проверяет, что доступ к профилю требует авторизации"""
        url = reverse("users:profile")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse("users:login"), resp["Location"])

    def test_profile_get_ok_when_logged_in(self):
        """Проверяет доступ к профилю авторизованного пользователя (GET-запрос)"""
        self.client.login(username=self.user.email, password=self.password)
        url = reverse("users:profile")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "users/profile.html")

    def test_profile_update_edits_current_user(self):
        """Проверяет обновление профиля авторизованного пользователя"""
        self.client.login(username=self.user.email, password=self.password)
        url = reverse("users:profile")

        data = {
            "first_name": "Tanya",
            "last_name": "Test",
            "phone": "+49123456789",
            "sex": getattr(self.user, "SexChoices", None).NOT_SPECIFIED if hasattr(self.user, "SexChoices") else "N",
            "date_of_birth": "1994-07-23",
        }

        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp["Location"], url)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Tanya")
        self.assertEqual(self.user.last_name, "Test")
        self.assertEqual(self.user.phone, "+49123456789")

        msgs = [m.message for m in get_messages(resp.wsgi_request)]
        self.assertIn("Профиль обновлён ✅", msgs)
