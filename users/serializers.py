from rest_framework import serializers
from users.models import User
from users.validators import CustomPhoneValidator
from django.contrib.auth import get_user_model
from services import send_email


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
    email = serializers.EmailField()

    def validate_email(self, email):
        """
        Проверяет валидность email.
        """
        if not email:
            raise serializers.ValidationError("Введите корректный email.")
        return email

    def create(self, validated_data):
        """
        Генерирует код для пользователя и отправляет его на email.
        """
        email = validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не найден.")

        # Генерируем код и отправляем
        raw_code = user.generate_code()
        send_email(email, raw_code)
        return {"detail": f"Код отправлен на почту {email}."}


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

    def validate(self, data):
        """
        Проверяет email и код.
        """
        email = data.get('email')
        code = data.get('code')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не найден.")

        if not user.is_code_valid():
            raise serializers.ValidationError("Код истёк или недействителен.")
        if user.code != code:
            raise serializers.ValidationError("Код неверный.")

        data['user'] = user
        return data

    def create(self, validated_data):
        """
        Завершает процесс авторизации.
        """
        user = validated_data['user']
        user.clear_code()  # Убираем код после успешной авторизации
        return user

# class OTPSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OTP
#         fields = "__all__"





