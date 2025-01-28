from django import forms
from users.models import User
from django.core.exceptions import ValidationError
from utils import check_number


class SendCodeForm(forms.Form):
    phone = forms.CharField(label="номер телефона", required=True)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        message = "Номер должен начинаться на цифру '7' и состоять из 11 цифр без дополнительных символов"
        if not check_number(phone):  # Используем ваш метод проверки
            raise ValidationError(
                "Номер должен начинаться на цифру '7' и состоять из 11 цифр без дополнительных символов"
            )
        return phone  # Возвращаем очищенное значение

    def save(self):
        # Логика сохранения пользователя
        phone = self.cleaned_data['phone']

        user, created = User.objects.get_or_create(phone=phone)
        return user


class VerifyCodeForm(forms.Form):
    phone = forms.CharField(label="номер телефона", required=True)
    code = forms.CharField(label="Код подтверждения", max_length=4, required=True)


class ActivateInviteCodeForm(forms.Form):
    invite_code = forms.CharField(
        max_length=6,
        label="Введите инвайт-код",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Инвайт-код"})
    )

