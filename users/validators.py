from django.core.validators import RegexValidator


phone_validator = RegexValidator(
    regex=r"^\+?[1-9]\d{7,14}$",
    message="Введите номер в начиная с '+', например +37112345678"
)
