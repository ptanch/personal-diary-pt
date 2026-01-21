from django.test import TestCase

from diary.forms import DiaryForm
from django.contrib.auth import get_user_model


User = get_user_model()


class DiaryFormTestCase(TestCase):
    """Тесты для формы DiaryForm"""
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="StrongPass123!"
        )

    def test_form_valid_with_normal_note(self):
        """Форма валидна, если note содержит текст"""
        form = DiaryForm(
            data={
                "title": "Заголовок",
                "note": "Это нормальная запись",
                "is_private": True,
            }
        )

        self.assertTrue(form.is_valid())

    def test_form_invalid_when_note_is_empty_string(self):
        """Пустая строка не проходит как обязательное поле"""
        form = DiaryForm(
            data={
                "title": "Заголовок",
                "note": "",
                "is_private": True,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("note", form.errors)
        self.assertEqual(form.errors["note"][0], "This field is required.")

    def test_form_invalid_when_note_is_only_spaces(self):
        """Нельзя сохранить запись из пробелов"""
        form = DiaryForm(
            data={
                "title": "Заголовок",
                "note": "     ",
                "is_private": True,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("note", form.errors)

    def test_form_invalid_when_note_is_only_newlines(self):
        """Нельзя сохранить запись из переносов строки"""
        form = DiaryForm(
            data={
                "title": "Заголовок",
                "note": "\n\n\n",
                "is_private": True,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("note", form.errors)
