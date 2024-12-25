import uuid

from django.contrib.auth import get_user_model
from posts.models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class CommentsViewSetTests(APITestCase):

    def setUp(self):
        # Создание пользователя
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

        # Создание поста для комментариев
        self.post = Post.objects.create(
            user=self.user,
            file_type="image/jpeg",
            file_key="somefilekey",
            created_at="2024-12-25",
        )

    def test_create_comment_for_post(self):
        # Создаем комментарий для поста
        data = {
            "post_id": self.post.post_id,
            "content": "This is a test comment",
        }

        response = self.client.post('/api/v1/posts/create/comment/', data)

        # Проверка успешного создания комментария
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], "This is a test comment")
        self.assertEqual(response.data['user']['username'], self.user.username)

    def test_create_nested_comment(self):
        # Создаем основной комментарий
        data = {
            "post_id": self.post.post_id,
            "content": "This is a parent comment",
        }
        response = self.client.post('/api/v1/posts/create/comment/', data)
        parent_comment_id = response.data['id']

        # Создаем вложенный комментарий
        nested_comment_data = {
            "parent_comment_id": str(parent_comment_id),
            "content": "This is a nested comment",
        }
        response = self.client.post(
            '/api/v1/posts/create/comment/',
            nested_comment_data,
        )

        # Проверка успешного создания вложенного комментария
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], "This is a nested comment")
        self.assertEqual(str(response.data['parent_comment_id']), parent_comment_id)

    def test_create_comment_with_both_post_and_parent_comment_id(self):
        # Попытка создания комментария с двумя полями: post_id и parent_comment_id
        data = {
            "post_id": self.post.post_id,
            "parent_comment_id": uuid.uuid4(),  # Некорректный parent_comment_id
            "content": "This should fail",
        }

        response = self.client.post('/api/v1/posts/create/comment/', data)

        # Проверка ошибки
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'You can only provide either post_id or parent_comment_id, not both.',
            str(response.data),
        )

    def test_create_comment_without_post_or_parent_comment(self):
        # Попытка создания комментария без указания post_id или parent_comment_id
        data = {
            "content": "This should also fail",
        }

        response = self.client.post('/api/v1/posts/create/comment/', data)

        # Проверка ошибки
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'You must provide either post_id or parent_comment_id.',
            str(response.data),
        )

    def test_list_comments_for_parent_comment(self):
        # Создаем комментарий и вложенный комментарий
        data = {
            "post_id": self.post.post_id,
            "content": "Parent comment",
        }
        response = self.client.post('/api/v1/posts/create/comment/', data)
        parent_comment_id = response.data['id']

        nested_data = {
            "parent_comment_id": parent_comment_id,
            "content": "Nested comment",
        }
        self.client.post('/api/v1/posts/create/comment/', nested_data)

        # Получаем комментарии для родительского комментария
        response = self.client.get(
            f'/api/v1/posts/?parent_comment_id={parent_comment_id}',
        )

        # Проверка получения вложенных комментариев
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
