from django.db import models

from config import settings


class Diary(models.Model):
    """Класс для представления дневника пользователя"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="diary_entries",
    )

    title = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Заголовок",
    )

    note = models.TextField(
        verbose_name="Запись",
        help_text="Напиши свои мысли здесь",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    is_private = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Запись дневника"
        verbose_name_plural = "Записи дневника"
        ordering = ("-created_at",)

    def __str__(self):
        base = self.title or self.note
        base = (base or "").strip()
        return (base[:50] + "…") if base else str(self.pk)
