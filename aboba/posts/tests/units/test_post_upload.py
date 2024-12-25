import tempfile
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.files import File
from posts.models import Post
from rest_framework import status
from rest_framework.test import (
    APIClient,
    APITestCase,
)
from rest_framework_simplejwt.tokens import RefreshToken


class TestPostViews(APITestCase):
    def setUp(self):
        """Set up the test environment."""
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            username='testuser',
        )

        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        self.post_data = {
            'file_type': 'image',
            'file_key': 'somefilekey',
        }
        self.post = Post.objects.create(user=self.user, **self.post_data)

    @mock.patch('posts.serializers.send_event_to_broker')
    @mock.patch('posts.serializers.upload_media_to_s3')
    def test_upload_meme_authenticated__success(self, *args):
        """Test upload meme functionality for authenticated users."""
        with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp_file:
            tmp_file.write(b"dummy file content")
            tmp_file.seek(0)
            uploaded_file = File(tmp_file)

            response = self.client.post(
                '/api/v1/posts/upload/',
                {'file': uploaded_file, 'file_type': 'image'},
                format='multipart',
            )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('file_key', response.data)
        self.assertIn('file_type', response.data)
        self.assertIn('created_at', response.data)

    def test_upload_meme_authenticated__error(self):
        """Test upload meme functionality for authenticated users."""
        with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp_file:
            tmp_file.write(b"dummy file content")
            tmp_file.seek(0)
            uploaded_file = File(tmp_file)

            response = self.client.post(
                '/api/v1/posts/upload/',
                {'file': uploaded_file, 'file_type': 'prikol'},
                format='multipart',
            )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_meme_unauthenticated(self):
        """Test upload meme functionality for unauthenticated users."""
        self.client.credentials()
        with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp_file:
            tmp_file.write(b"dummy file content")
            tmp_file.seek(0)
            uploaded_file = File(tmp_file)

            response = self.client.post(
                '/api/v1/posts/upload/',
                {'file': uploaded_file},
                format='multipart',
            )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
