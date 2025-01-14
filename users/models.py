from django.db import models
from django.contrib.auth.models import AbstractUser
import random
from django.utils import timezone
from datetime import timedelta

from utils import NULLABLE


class User(AbstractUser):
    username = None
    phone = models.CharField(verbose_name="номер телефона", max_length=15)
    email = models.EmailField(verbose_name="почта", unique=True, **NULLABLE)
    code = models.CharField(verbose_name="код подтверждения", max_length=4, **NULLABLE)
    code_created_at = models.DateTimeField(verbose_name="время создания кода", **NULLABLE)
    code_is_active = models.BooleanField(verbose_name="активность кода", default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def generate_code(self):
        """
        Генерирует 4-значный код, сохраняет его как пароль и в поле `code`.
        """
        raw_code = str(random.randint(1000, 9999))
        self.code = raw_code  # Сохраняем код в поле `code`
        self.set_password(raw_code)  # Хэшируем код как пароль
        self.code_created_at = timezone.now()  # Устанавливаем время создания кода
        self.code_is_active = True
        self.save()
        return raw_code  # Возвращаем незашифрованный код

    def is_code_valid(self):
        """
        Проверяет, действителен ли код.
        """
        if not self.code_created_at:
            return False

        # Проверяем, истёк ли срок действия кода
        if timezone.now() > self.code_created_at + timedelta(minutes=5):
            self.code_is_active = False  # Деактивируем код
            self.save()
            return False

        return self.code_is_active

    def clear_code(self):
        """
        Очищает код после успешного применения.
        """
        self.code = None
        self.code_created_at = None
        self.code_is_active = False  # Деактивируем код
        self.save()

# class OTP(models.Model):
#     phone_number = models.CharField(max_length=15, verbose_name="номер телефона")
#     code = models.CharField(verbose_name="код подтверждения", max_length=4)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_used = models.BooleanField(default=False)
#
#     def is_valid(self):
#         return timezone.now() < self.created_at + timedelta(minutes=5) and not self.is_used
#
#     def __str__(self):
#         return f"{self.phone_number} - {self.code}"

