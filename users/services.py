import random
from django.core.mail import send_mail
from users.tasks import cancel_code_activity

from users.models import User


def generate_code():
    """ генерация четырехзначного кода из цифр """
    return str(random.randint(1000, 9999))


def send_email(email, code):
    send_mail(
        "Ваш код для авторизации",
        code,
        "counter230620013@yandex.com",
        [email]
    )
    user = User.objects.get(email=email)
    cancel_code_activity.apply_async((user.id,), countdown=5 * 60)
    print('отправлено сообщение на почту!!!!!!')


