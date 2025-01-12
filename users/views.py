from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import VerifyCodeSerializer


from rest_framework import generics
from .serializers import SendCodeSerializer


class SendCodeAPIView(generics.CreateAPIView):
    serializer_class = SendCodeSerializer


class VerifyCodeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        # Генерируем токен для пользователя
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


# class UserCreateAPIView(generics.CreateAPIView):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#
#     def perform_create(self, serializer):
#         user = serializer.save()
#
#
# class OTPCreateAPIView(generics.CreateAPIView):
#     serializer_class = OTPSerializer
#     queryset = OTP.objects.all()
