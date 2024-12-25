import uuid
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase


class UploadMemeMemeViewSetTestCase(APITestCase):
    def setUp(self):
        username = f"testuser_{uuid.uuid4()}"
        password = 'pass123'
        email = f'testemail_{uuid.uuid4()}@bot.ru'
        self.user = get_user_model().objects.create_user(
            username=username,
            password=password,
            email=email,
        )

        # Авторизуем пользователя по умолчанию
        self.client.force_authenticate(user=self.user)

    def test_create_meme(self):
        image_data = BytesIO(b"image data")
        image_data.name = 'test_image.jpg'
        image = InMemoryUploadedFile(
            image_data,
            None,
            'test_image.jpg',
            'image/jpeg',
            len(image_data.getvalue()),
            None,
        )

        data = {
            'file': image,
            'file_type': 'image',
        }

        # Отправляем запрос с авторизацией
        response = self.client.post('/api/v1/posts/upload/', data, format='multipart')

        # Проверка успешного ответа
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('post_id', response.data)
        self.assertIn('file_key', response.data)
        self.assertIn('file_type', response.data)
        self.assertIn('created_at', response.data)
