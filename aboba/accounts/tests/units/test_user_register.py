from unittest.mock import patch

from aboba.accounts.views import RegisterViewSet
from django.test import (
    RequestFactory,
    TransactionTestCase,
)
from rest_framework import status
from rest_framework.response import Response


class TestUserRegistration(TransactionTestCase):

    @patch('aboba.accounts.views.RegisterViewSet.create')
    def test_register_user__success(self, mock_post):
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
            format='json',
        )

        register_view = RegisterViewSet.as_view({"post": "create"})

        response = register_view(request=request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('aboba.accounts.views.RegisterViewSet.create')
    def test_register_user__error(self, mock_post):
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

        register_view = RegisterViewSet.as_view({"post": "create"})

        response = register_view(request=request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
