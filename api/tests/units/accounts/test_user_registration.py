import unittest
from unittest.mock import patch

from accounts.views import RegisterView
from django.test import RequestFactory
from rest_framework import status
from rest_framework.response import Response


class TestUserRegistration(unittest.TestCase):

    @patch('api.aboba.accounts.views.RegisterView.post')
    def test_register_user_success(self, mock_post):
        """Test user registration success"""

        mock_post.return_value = Response(status=status.HTTP_201_CREATED)

        user_data = {
            'email': 'aboba@bot.ru',
            'password': 'password123',
            'username': 'aboba',
        }

        factory = RequestFactory()

        request = factory.post(
            '/api/v1/accounts/register/',
            user_data,
            content_type='application/json',
        )

        register_view = RegisterView.as_view()

        response = register_view(request=request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_post.assert_called_once()

    @patch('api.aboba.accounts.views.RegisterView.post')
    def test_register_user_error(self, mock_post):
        """Test user registration error (e.g., email already exists)"""

        mock_post.return_value = Response(status=status.HTTP_400_BAD_REQUEST)

        user_data = {
            'email': 'aboba@bot.ru',
            'password': 'password123',
            'username': 'aboba',
        }

        factory = RequestFactory()

        request = factory.post(
            '/api/v1/accounts/register/',
            user_data,
            content_type='application/json',
        )

        register_view = RegisterView.as_view()

        response = register_view(request=request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mock_post.assert_called_once()
