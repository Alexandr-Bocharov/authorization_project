import random
from django.core.mail import send_mail


def generate_code():
    return str(random.randint(1000, 9999))


def send_email(email, code):
    send_mail(
        "Ваш код для авторизации",
        code,
        "counter230620013@yandex.com",
        [email]
    )

