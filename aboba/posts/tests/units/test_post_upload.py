import uuid
from io import BytesIO
from unittest.mock import patch

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

        self.client.force_authenticate(user=self.user)

    @patch('posts.serializers.upload_media_to_s3')
    def test_create_meme(self, mock_upload):
        # Создание изображения для загрузки
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

        response = self.client.post('/api/v1/posts/upload/', data, format='multipart')

        # Проверка успешного ответа
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('post_id', response.data)
        self.assertIn('file_key', response.data)
        self.assertIn('file_type', response.data)
        self.assertIn('created_at', response.data)
