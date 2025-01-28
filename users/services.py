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


def send_sms(phone, code):
    """ Реальная рассылка через сервис SMS aero """
    username = os.getenv("SMS_AERO_USER")
    password = os.getenv("SMS_AERO_KEY")

    response = requests.get(
        f"https://email:api_key@gate.smsaero.ru/v2/sms/send?number={phone}&text=your+code:+{code}&sign=SMS Aero",
        auth=HTTPBasicAuth(username, password)
    )

    user = User.objects.get(phone=phone)
    cancel_code_activity.apply_async((user.id,), countdown=10 * 60)  # код перестанет быть активным через 10 минут,
                                                                    # если его не ввести


def send_sms_imitation(phone, code):
    """ Имитация смс-рассылки """

    user = User.objects.get(phone=phone)
    cancel_code_activity.apply_async((user.id,), countdown=10 * 60)  # код перестанет быть активным через 10 минут,
                                                                    # если его не ввести
    print(f"смс отправлено на номер {phone} с кодом {code}")



