from rest_framework import serializers
from utils import check_number


class CustomPhoneValidator:

    def __call__(self, value):
        message = "Номер должен начинаться на цифру '7' и состоять из 11 цифр без дополнительных символов"
        phone_number = value.get('phone')

        if not check_number(phone_number):
            raise serializers.ValidationError(message)
