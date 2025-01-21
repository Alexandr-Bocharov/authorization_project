from rest_framework import serializers
from users.models import User
from users.validators import CustomPhoneValidator
from users.services import send_sms, send_sms_imitation


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
    phone = serializers.CharField(required=True)

    class Meta:
        validators = [
            CustomPhoneValidator(),
        ]

    def create(self, validated_data):
        """
        Генерирует код для пользователя и отправляет его на email.
        """
        phone = validated_data['phone']
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            user = User.objects.create(phone=phone)

        # Генерируем код и отправляем
        raw_code = user.generate_code()
        # send_sms(phone, raw_code)
        send_sms_imitation(phone, raw_code)
        return user


class VerifyCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()

    def validate(self, data):
        """
        Проверяет email и код.
        """
        phone = data.get('phone')
        code = data.get('code')

        try:
            user = User.objects.get(phone=phone)
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





