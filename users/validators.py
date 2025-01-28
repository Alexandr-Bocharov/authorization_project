from rest_framework import serializers
from utils import check_number
from django.core.exceptions import ValidationError


class CustomPhoneValidator:

    def __call__(self, value):
        message = "Номер должен начинаться на цифру '7' и состоять из 11 цифр без дополнительных символов"
        phone_number = value.get('phone')

        if phone_number:
            if not check_number(phone_number):
                raise serializers.ValidationError(message)


def validate_phone(value):
    message = "Номер должен начинаться на цифру '7' и состоять из 11 цифр без дополнительных символов"
    if not check_number(value):  # Ваш метод для проверки номера
        raise ValidationError(message)


