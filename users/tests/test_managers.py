from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserManagerTestCase(TestCase):
    def test_create_user_without_email_raises(self):
        """
        Проверяет, что при создании обычного пользователя без указания email
        выбрасывается исключение ValueError
        """
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="StrongPass123!")

    def test_create_superuser_sets_flags(self):
        """Проверяет корректность установки флагов при создании суперпользователя"""
        su = User.objects.create_superuser(email="admin@example.com", password="StrongPass123!")
        self.assertTrue(su.is_staff)
        self.assertTrue(su.is_superuser)
        self.assertTrue(su.is_active)
