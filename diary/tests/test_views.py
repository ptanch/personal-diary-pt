from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from diary.models import Diary


User = get_user_model()


class DiaryViewsTestCase(TestCase):
    """Тесты для контроллеров DiaryView"""
    def setUp(self):
        self.user = User.objects.create_user(email="u1@example.com", password="StrongPass123!")
        self.other = User.objects.create_user(email="u2@example.com", password="StrongPass123!")

    def test_list_requires_login(self):
        """Проверяет, что просмотр списка записей дневника требует авторизации"""
        url = reverse("diary:diary_list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        # редирект на login с ?next=
        self.assertIn(reverse("users:login"), resp["Location"])

    def test_create_requires_login(self):
        """Проверяет, что создание записи дневника требует авторизации"""
        url = reverse("diary:diary_create")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse("users:login"), resp["Location"])

    def test_authenticated_can_create_entry_and_owner_is_set(self):
        """
        Проверяет, что авторизованный пользователь может создать запись дневника,
        и при этом корректно устанавливается владелец записи
        """
        self.client.login(email="u1@example.com", password="StrongPass123!")
        url = reverse("diary:diary_create")

        data = {"title": "Test", "note": "Hello", "is_private": True}
        resp = self.client.post(url, data=data)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Diary.objects.count(), 1)

        entry = Diary.objects.first()
        self.assertEqual(entry.user, self.user)
        self.assertEqual(entry.title, "Test")
        self.assertEqual(entry.note, "Hello")

    def test_user_can_view_own_detail(self):
        """Проверяет, что пользователь может просмотреть детальную информацию о своей записи"""
        entry = Diary.objects.create(user=self.user, title="Mine", note="Text", is_private=True)
        self.client.login(email="u1@example.com", password="StrongPass123!")
        url = reverse("diary:diary_detail", kwargs={"pk": entry.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Mine")

    def test_user_cannot_view_other_users_detail(self):
        """Проверяет, что пользователь не может просмотреть детальную информацию о записи другого пользователя"""
        entry = Diary.objects.create(user=self.other, title="Other", note="Text", is_private=True)
        self.client.login(email="u1@example.com", password="StrongPass123!")
        url = reverse("diary:diary_detail", kwargs={"pk": entry.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    def test_user_can_update_own_entry(self):
        """Проверяет, что пользователь может обновить свою запись дневника"""
        entry = Diary.objects.create(user=self.user, title="Old", note="Text", is_private=True)
        self.client.login(email="u1@example.com", password="StrongPass123!")
        url = reverse("diary:diary_update", kwargs={"pk": entry.pk})

        resp = self.client.post(url, data={"title": "New", "note": "Updated", "is_private": False})
        self.assertEqual(resp.status_code, 302)

        entry.refresh_from_db()
        self.assertEqual(entry.title, "New")
        self.assertEqual(entry.note, "Updated")
        self.assertFalse(entry.is_private)

    def test_user_cannot_update_other_users_entry(self):
        """Проверяет, что пользователь не может обновить запись другого пользователя"""
        entry = Diary.objects.create(user=self.other, title="Other", note="Text", is_private=True)
        self.client.login(email="u1@example.com", password="StrongPass123!")
        url = reverse("diary:diary_update", kwargs={"pk": entry.pk})
        resp = self.client.post(url, data={"title": "Hack", "note": "Hack", "is_private": True})
        self.assertEqual(resp.status_code, 404)

    def test_user_can_delete_own_entry(self):
        """Проверяет, что пользователь может удалить свою запись дневника"""
        entry = Diary.objects.create(user=self.user, title="Del", note="Text", is_private=True)
        self.client.login(email="u1@example.com", password="StrongPass123!")
        url = reverse("diary:diary_delete", kwargs={"pk": entry.pk})

        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Diary.objects.filter(pk=entry.pk).exists())

    def test_user_cannot_delete_other_users_entry(self):
        """Проверяет, что пользователь не может удалить запись другого пользователя"""
        entry = Diary.objects.create(user=self.other, title="Other", note="Text", is_private=True)
        self.client.login(email="u1@example.com", password="StrongPass123!")
        url = reverse("diary:diary_delete", kwargs={"pk": entry.pk})

        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 404)
        self.assertTrue(Diary.objects.filter(pk=entry.pk).exists())

    def test_search_filters_by_title_or_note(self):
        """Проверяет, что поиск фильтрует записи по заголовку или содержимому заметки"""
        Diary.objects.create(user=self.user, title="Котики", note="про жизнь", is_private=True)
        Diary.objects.create(user=self.user, title="Работа", note="котики тоже бывают на работе", is_private=True)
        Diary.objects.create(user=self.user, title="Погода", note="дождь", is_private=True)

        self.client.login(email="u1@example.com", password="StrongPass123!")
        url = reverse("diary:diary_list")

        resp = self.client.get(url, {"q": "котики"})
        self.assertEqual(resp.status_code, 200)

        entries = resp.context["entries"]
        self.assertEqual(entries.count(), 2)

    def test_pagination_9_per_page(self):
        """Проверяет, что ожидаемое кол-во записей на одной странице 9"""
        # 12 записей -> 9 на первой странице
        Diary.objects.bulk_create([
            Diary(user=self.user, title=f"T{i}", note="N", is_private=True)
            for i in range(12)
        ])

        self.client.login(email="u1@example.com", password="StrongPass123!")
        url = reverse("diary:diary_list")

        resp1 = self.client.get(url)
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(len(resp1.context["entries"]), 9)

        resp2 = self.client.get(url, {"page": 2})
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(len(resp2.context["entries"]), 3)
