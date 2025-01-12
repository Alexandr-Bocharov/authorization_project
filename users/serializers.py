from rest_framework import serializers
from users.models import User, OTP
from users.validators import CustomPhoneValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        validators = [
            CustomPhoneValidator()
        ]


# class OTPSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OTP
#         fields = "__all__"


