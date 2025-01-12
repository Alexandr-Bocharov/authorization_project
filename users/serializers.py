from rest_framework import serializers
from users.models import User
from users.validators import CustomPhoneValidator
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        validators = [
            CustomPhoneValidator()
        ]

    def create(self, validated_data):
        """
        Генерация кода при создании пользователя.
        """
        user = super().create(validated_data)
        raw_code = user.generate_code()  # Генерация и сохранение кода
        # Здесь вы можете добавить отправку SMS с кодом
        print(f"Отправлен код: {raw_code}")  # Имитация отправки
        return user


User = get_user_model()


class SendCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate_phone(self, phone):
        """
        Проверяет валидность номера телефона.
        """
        if not phone.isdigit() or len(phone) < 10:  # Пример валидации
            raise serializers.ValidationError("Введите корректный номер телефона.")
        return phone

    def create(self, validated_data):
        """
        Генерирует код для пользователя.
        """
        phone = validated_data['phone']
        user, created = User.objects.get_or_create(phone=phone)
        raw_code = user.generate_code()  # Генерация кода
        # Здесь можно добавить отправку SMS
        print(f"Код отправлен на номер {phone}: {raw_code}")
        return user


class VerifyCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()

    def validate(self, data):
        """
        Проверяет телефон и код.
        """
        phone = data.get('phone')
        code = data.get('code')

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким номером телефона не найден.")

        if not user.is_code_valid():
            raise serializers.ValidationError("Код истёк или недействителен.")
        if user.code != code:
            raise serializers.ValidationError("Код неверный.")

        return user

    def create(self, validated_data):
        """
        Завершает процесс авторизации.
        """
        user = validated_data
        user.clear_code()  # Убираем код после успешной авторизации
        return user

# class OTPSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OTP
#         fields = "__all__"





