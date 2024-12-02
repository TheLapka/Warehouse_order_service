import uuid
from datetime import date

from apps.user_and_email_manager.managers import CustomUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Custom User model."""

    first_name = models.CharField(max_length=150, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=150, blank=True, verbose_name="Фамилия")
    surname = models.CharField(max_length=150, blank=True, verbose_name="Отчество")
    username = None

    email = models.EmailField(verbose_name="E-mail", unique=True)
    customer_id = models.UUIDField(
        default=uuid.uuid4, unique=True, verbose_name="ЛичныйID"
    )
    is_confired = models.BooleanField(
        verbose_name="Подтверждение аккаунта", default=False
    )
    date_of_birth = models.DateField(default=date.today, verbose_name="День рождения")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: CustomUserManager = CustomUserManager()

    def __str__(self):
        return self.email
