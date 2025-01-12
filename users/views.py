from django.shortcuts import render
from rest_framework import generics

from users.models import User, OTP
from users.serializers import UserSerializer, OTPSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class OTPCreateAPIView(generics.CreateAPIView):
    serializer_class = OTPSerializer
    queryset = OTP.objects.all()
