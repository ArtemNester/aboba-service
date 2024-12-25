from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


class LoginViewSetTests(TestCase):
    @classmethod
    def setUpClass(cls):
        User.objects.create_user(
            username='testuser',
            email='aboba@bot.ru',
            password='testpass',
        )
        super().setUpClass()

    def setUp(self):
        self.client = APIClient()

    @patch('accounts.views.LoginViewSet.create')
    def test_login_in_user_successfully(self, mock_create):
        mock_create.return_value = Response(status=status.HTTP_200_OK)
        response = self.client.post(
            '/api/v1/accounts/login/',
            {'email': 'aboba@bot.ru', 'password': 'testpass'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_handles_invalid_login(self):
        response = self.client.post(
            '/api/v1/accounts/login/',
            {'email': 'aboba@bot.ru', 'password': 'wrongpass'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
