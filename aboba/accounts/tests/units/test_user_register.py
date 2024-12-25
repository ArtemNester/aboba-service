from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class RegisterViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user_successfully(self):
        response = self.client.post(
            '/api/v1/accounts/register/',
            {
                'username': 'newuser',
                'email': 'newuser@bot.ru',
                'password1': 'newpassword',
                'password2': 'newpassword',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        # Проверяем, что пользователь был создан
        user = User.objects.get(username='newuser')
        self.assertEqual(user.email, 'newuser@bot.ru')

    def test_register_user_with_missing_fields(self):
        response = self.client.post(
            '/api/v1/accounts/register/',
            {
                'username': 'newuser',
                'email': 'newuser@bot.ru',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password1', response.data)
        self.assertIn('password2', response.data)

    def test_register_user_with_invalid_email(self):
        response = self.client.post(
            '/api/v1/accounts/register/',
            {
                'username': 'newuser',
                'email': 'invalid-email',
                'password1': 'newpassword',
                'password2': 'newpassword',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
