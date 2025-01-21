from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from users.models import User


class SendCodeAPITestCase(APITestCase):

    def setUp(self):
        self.url = reverse("users:send-code")
        self.valid_phone = "79999999999"
        self.invalid_phone = "799999999991"

    def test_send_code_success(self):
        """ Тест успешной отправки кода с корректным номером телефона. """
        response = self.client.post(self.url, {"phone": self.valid_phone})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(phone=self.valid_phone).exists())
        user = User.objects.get(phone=self.valid_phone)
        self.assertIsNotNone(user.code)  # проверяем, записался ли созданный код

    def test_send_code_invalid_phone(self):
        """ Тест обработки некорректного номера телефона. """
        response = self.client.post(self.url, {"phone": self.invalid_phone})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(phone=self.invalid_phone).exists())
        self.assertEqual(response.data,
                         {'non_field_errors': [ErrorDetail(string="Номер должен начинаться на цифру '7' и состоять из 11 цифр без дополнительных символов", code='invalid')]}
)

    def test_send_code_existing_user(self):
        """ Тест отправки кода уже существующему пользователю """
        user = User.objects.create(phone=self.valid_phone)
        response = self.client.post(self.url, {"phone": self.valid_phone})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user.refresh_from_db()
        self.assertIsNotNone(user.code)


class VerifyCodeAPITestCase(APITestCase):

    def setUp(self):
        self.url = reverse("users:verify-code")
        self.phone = "79999999999"
        self.user = User.objects.create(phone=self.phone)
        self.user.generate_code()

    def test_verify_code_success(self):
        """ Тест успешной верификации четырехзначного кода, который пришел в смс """
        response = self.client.post(self.url, {"phone": self.phone,
                                               "code": self.user.code})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_verify_code_invalid(self):
        """ Тест неуспешной верификации четырехзначного кода, который пришел в смс """
        response = self.client.post(self.url, {"phone": self.phone,
                                               "code": "0000"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,
                         {'non_field_errors': [ErrorDetail(string='Код неверный.', code='invalid')]}
)


class UserAPITestCase(APITestCase):

    def setUp(self):
        self.phone = "79999999999"
        self.user = User.objects.create(phone=self.phone)

    def test_user_retrieve(self):
        url = reverse("users:user-detail", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("phone"), self.phone)

    def test_user_list(self):
        url = reverse("users:users")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0].get("phone"), self.phone)

    def test_user_update_successful(self):
        """ Тест user-update на аутентифицированном пользователе """
        self.client.force_authenticate(user=self.user)
        url = reverse("users:user-update", args=(self.user.id,))
        data = {"email": "admin@sky.pro"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), response.data.get("email"))

    def test_user_update_unsuccessful(self):
        """ Тест user-update на пользователе, который не вошел в систему """
        url = reverse("users:user-update", args=(self.user.id,))
        data = {"email": "admin@sky.pro"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)






