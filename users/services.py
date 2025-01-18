import os
import random
from django.core.mail import send_mail
from users.tasks import cancel_code_activity
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

from users.models import User


load_dotenv()


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


def send_sms(phone, code):
    username = os.getenv("SMS_AERO_USER")
    password = os.getenv("SMS_AERO_KEY")

    response = requests.get(f"https://email:api_key@gate.smsaero.ru/v2/sms/send?number={phone}&text=your+code:+{code}&sign=SMS Aero",
                            auth=HTTPBasicAuth(username, password))

    user = User.objects.get(phone=phone)
    cancel_code_activity.apply_async((user.id,), countdown=5 * 60)


