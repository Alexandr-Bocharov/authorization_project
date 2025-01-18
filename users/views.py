from django.contrib.auth import login
from django.middleware.csrf import rotate_token
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSerializer, UserProfileSerializer, ActivateInviteCodeSerializer

from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsOwner
from .serializers import VerifyCodeSerializer


from rest_framework import generics
from .serializers import SendCodeSerializer

from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import User
from users.forms import SendCodeForm, ActivateInviteCodeForm

from .services import send_email

from django.contrib import messages
from .forms import VerifyCodeForm



class SendCodeAPIView(generics.CreateAPIView):
    serializer_class = SendCodeSerializer


class VerifyCodeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)   # генерируем токены для пользователя
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [
        IsAuthenticated,
        IsOwner,
    ]


class ActivateInviteCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Активирует инвайт-код.
        """
        serializer = ActivateInviteCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(request.user)
        return Response({"message": "Инвайт-код успешно активирован."}, status=status.HTTP_200_OK)


class ActivateInviteCodeTempView(FormView):
    template_name = "users/activate_invite_code.html"
    form_class = ActivateInviteCodeForm

    def form_valid(self, form):
        invite_code = form.cleaned_data['invite_code']
        user = self.request.user

        # Используем сериализатор для проверки и активации инвайт-кода
        serializer = ActivateInviteCodeSerializer(data={"invite_code": invite_code})
        serializer.is_valid(raise_exception=False)

        if serializer.errors:
            messages.error(self.request, "Инвайт-код не существует.")
            return self.form_invalid(form)

        try:
            serializer.save(user=user)
            messages.success(self.request, "Инвайт-код успешно активирован!")
            return redirect("users:profile-temp", pk=user.id)  # Перенаправление на профиль
        except serializers.ValidationError as e:
            messages.error(self.request, e.detail)
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Некорректные данные. Попробуйте снова.")
        return super().form_invalid(form)


class SendCodeView(FormView):
    template_name = "users/send_code.html"
    form_class = SendCodeForm

    def form_valid(self, form):
        user = form.save()
        email = user.email
        code = user.generate_code()
        user.code = code
        send_email(email, code)
        user.save()
        return redirect(f"{reverse('users:verify-code-temp')}?email={user.email}")

    def form_invalid(self, form):
        return HttpResponse("Некорректные данные", status=400)


class Home(ListView):
    template_name = "users/base.html"
    model = User


class VerifyCodeView(FormView):
    template_name = 'users/verify_code.html'  # Шаблон для отображения формы
    form_class = VerifyCodeForm  # Форма, связанная с этим представлением

    def get_initial(self):

    # Заполняем поле email из GET-параметров
        initial = super().get_initial()
        initial['email'] = self.request.GET.get('email', '')
        return initial

    def form_valid(self, form):
        # Получаем данные из формы
        code = form.cleaned_data['code']
        email = form.cleaned_data['email']

        try:
            # Проверяем пользователя и код
            user = User.objects.get(email=email, code=code)
            print(user.code_is_active)
            if not user.code_is_active:
                messages.error(self.request, "Код истёк. Запросите новый код.")
                return self.form_invalid(form)

            # Успешная проверка, очищаем код и генерируем токены
            user.clear_code()

            login(self.request, user)

            rotate_token(self.request)

            refresh = RefreshToken.for_user(user)

            # Отправляем токены на страницу или сохраняем в сессии
            messages.success(self.request, "Код подтвержден. Вы успешно авторизовались.")
            self.request.session['access_token'] = str(refresh.access_token)
            self.request.session['refresh_token'] = str(refresh)

            return redirect(reverse('users:profile-temp', kwargs={"pk": user.id}))  # Перенаправление на страницу профиля

        except User.DoesNotExist:
            messages.error(self.request, "Неправильный код или email.")
            return self.form_invalid(form)

    def form_invalid(self, form):
        # Обработка неуспешной проверки формы
        return super().form_invalid(form)


class UserDetailView(DetailView):
    template_name = "users/user_detail.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        serializer = UserProfileSerializer(user)
        context["user_profile"] = serializer.data
        return context


