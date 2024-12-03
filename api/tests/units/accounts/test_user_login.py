import unittest
from unittest.mock import patch

from aboba.accounts.views import LoginView
from django.test import RequestFactory
from rest_framework import status
from rest_framework.response import Response


class TestUserLogin(unittest.TestCase):

    @patch('api.aboba.accounts.views.LoginView.post')
    def test_login_user__success(self, mock_post):
        """Test user login success"""

        mock_post.return_value = Response(status=status.HTTP_200_OK)

        user_data = {'email': 'aboba@bot.ru', 'password': 'password123'}

        factory = RequestFactory()

        request = factory.post(
            '/api/v1/accounts/login/',
            user_data,
            content_type='application/json',
        )

        login_view = LoginView.as_view()

        response = login_view(request=request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_post.assert_called_once()

    @patch('api.aboba.accounts.views.LoginView.post')
    def test_login_user__error(self, mock_post):
        """Test user login error"""

        mock_post.return_value = Response(status=status.HTTP_400_BAD_REQUEST)

        user_data = {'email': 'aboba@bot.ru', 'password': 'wrongpassword'}

        factory = RequestFactory()

        request = factory.post(
            '/api/v1/accounts/login/',
            user_data,
            content_type='application/json',
        )

        login_view = LoginView.as_view()

        response = login_view(request=request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mock_post.assert_called_once()
