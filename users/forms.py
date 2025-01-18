from django import forms

from users.models import User


class SendCodeForm(forms.Form):
    email = forms.EmailField(label="почта", required=True)

    def save(self):
        # Логика сохранения пользователя
        email = self.cleaned_data['email']
        user, created = User.objects.get_or_create(email=email)
        return user


class VerifyCodeForm(forms.Form):
    email = forms.EmailField(label="Email", required=True)
    code = forms.CharField(label="Код подтверждения", max_length=4, required=True)


class ActivateInviteCodeForm(forms.Form):
    invite_code = forms.CharField(
        max_length=6,
        label="Введите инвайт-код",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Инвайт-код"})
    )

