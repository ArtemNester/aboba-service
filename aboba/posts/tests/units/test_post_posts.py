from unittest.mock import (
    MagicMock,
    patch,
)

import pytest
from django.contrib.auth.models import User
from django.test import TestCase
from posts.models import Post
from posts.views import PostsViewSet
from rest_framework import status


class PostsViewSetTests(TestCase):

    @pytest.mark.django_db
    def setUp(self):
        self.user = User.objects.create_user(
            username=f'testuser_{self.__class__.test_retrieves_single_post_successfully.__name__}',
            email='aboba@bot.ru',
            password='testpass',
        )

    @patch('posts.views.PostResponseSerializer')
    @pytest.mark.django_db
    def test_retrieves_single_post_successfully(self, mock_serializer):
        post = Post.objects.create(
            user=self.user,
            file_type='image/jpeg',
            file_key='somefilekey',
            created_at='2024-12-25',
        )

        serializer_instance = mock_serializer.return_value
        serializer_instance.data = {
            'post_id': str(post.post_id),
            'file_type': post.file_type,
            'file_key': post.file_key,
            'created_at': post.created_at,
            'user': {'username': self.user.username},
            'post_comments': [],
        }

        # Имитируем запрос
        viewset = PostsViewSet()
        request = MagicMock()
        request.query_params = {
            'post_id': str(post.post_id),
        }  # Также преобразуем сюда UUID в строку
        viewset.request = request
        viewset.format_kwarg = None

        # Запускаем метод list
        response = viewset.list(request)

        # Проверки
        self.assertEqual(response.status_code, status.HTTP_200_OK)
