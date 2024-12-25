from unittest.mock import patch

from aboba.accounts.views import LoginViewSet
from django.test import (
    RequestFactory,
    TransactionTestCase,
)
from rest_framework import status
from rest_framework.response import Response


class TestUserLogin(TransactionTestCase):
    @patch('aboba.accounts.views.LoginViewSet.create')
    def test_login_user__success(self, mock_create):
        """Тест успешного логина пользователя"""

        mock_create.return_value = Response(status=status.HTTP_200_OK)

        user_data = {
            'email': 'aboba@bot.ru',
            'password': 'password123',
        }

        factory = RequestFactory()

        request = factory.post(
            '/api/v1/accounts/login/',
            user_data,
            content_type='application/json',
        )

        login_view = LoginViewSet.as_view({"post": "create"})

        response = login_view(request=request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('aboba.accounts.views.LoginViewSet.create')
    def test_login_user__error(self, mock_create):
        """Тест ошибки логина (например, неверный пароль)"""

        mock_create.return_value = Response(status=status.HTTP_400_BAD_REQUEST)

        user_data = {
            'email': 'aboba@bot.ru',
            'password': 'wrongpassword',
        }

        factory = RequestFactory()

        request = factory.post(
            '/api/v1/accounts/login/',
            user_data,
            content_type='application/json',
        )

        login_view = LoginViewSet.as_view({"post": "create"})

        response = login_view(request=request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
