from rest_framework import serializers, status
from rest_framework.response import Response
from users.permissions import IsOwner
from users.models import User
from users.validators import CustomPhoneValidator
from django.contrib.auth import get_user_model
from users.services import send_email


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
        validators = [
            CustomPhoneValidator(),
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    phone_numbers_activated_by_invite = serializers.SerializerMethodField()

    class Meta:
        model = User
        # fields = ['id', 'email', 'invite_code', 'activated_invite_code', 'phone_numbers_activated_by_invite']
        fields = "__all__"

    def get_phone_numbers_activated_by_invite(self, obj):
        """
        Получает список номеров телефонов пользователей, которые активировали инвайт-код текущего пользователя.
        """
        users = User.objects.filter(activated_invite_code=obj.invite_code)
        return [user.phone for user in users if user.phone]


class ActivateInviteCodeSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=6)

    def validate_invite_code(self, invite_code):
        """
        Проверяем существование инвайт-кода в системе.
        """
        if not User.objects.filter(invite_code=invite_code).exists():
            raise serializers.ValidationError("Инвайт-код не существует.")
        return invite_code

    def save(self, user):
        """
        Активируем инвайт-код для текущего пользователя.
        """
        invite_code = self.validated_data['invite_code']
        if user.activated_invite_code:
            raise serializers.ValidationError("Вы уже активировали инвайт-код.")
        user.activated_invite_code = invite_code
        user.save()
        return user






class SendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

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
        print("REQUEST DATA:", validated_data)
        email = validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create(email=email)

        # Генерируем код и отправляем
        raw_code = user.generate_code()
        send_email(email, raw_code)
        return user


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





