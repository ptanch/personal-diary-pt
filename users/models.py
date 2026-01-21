from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import UserManager
from users.validators import phone_validator


class User(AbstractUser):
    """Класс для представления пользователя"""

    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите свою почту"
    )

    class SexChoices(models.TextChoices):
        MALE = "M", "Мужской"
        FEMALE = "F", "Женский"
        OTHER = "O", "Другой"
        NOT_SPECIFIED = "N", "Не указан"

    sex = models.CharField(
        max_length=1, choices=SexChoices.choices, default=SexChoices.NOT_SPECIFIED
    )

    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Имя",
        help_text="Введите Ваше имя",
    )

    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Фамилия",
        help_text="Введите Вашу фамилию",
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Введите свой номер телефона",
        validators=[phone_validator],
    )

    date_of_birth = models.DateField(
        null=True, blank=True, verbose_name="Дата рождения"
    )

    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватарка",
        help_text="Загрузите свое фото",
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email or str(self.pk)
