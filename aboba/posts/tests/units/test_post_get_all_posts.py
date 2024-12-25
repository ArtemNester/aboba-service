from django.contrib.auth import get_user_model
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

    def test_list_all_posts_authenticated(self):
        """Тест получения всех постов для аутентифицированных пользователей."""
        response = self.client.get('/api/v1/posts/get/all/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_list_all_posts_unauthenticated(self):
        """Тест получения всех постов для неаутентифицированных пользователей."""
        self.client.credentials()
        response = self.client.get('/api/v1/posts/get/all/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
