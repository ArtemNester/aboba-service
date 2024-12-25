import unittest
from unittest.mock import (
    MagicMock,
    patch,
)

from posts.views import PostsViewSet
from rest_framework import status


class PostsViewSetTests(unittest.TestCase):
    @patch('posts.views.PostResponseSerializer')
    def test_lists_all_posts_successfully(self, mock_serializer):
        viewset = PostsViewSet()
        request = MagicMock()
        queryset = MagicMock()
        viewset.filter_queryset = MagicMock(return_value=queryset)
        serializer_instance = mock_serializer.return_value
        serializer_instance.data = [{'id': 1, 'title': 'test'}]

        response = viewset.list(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{'id': 1, 'title': 'test'}])

    @patch('posts.views.PostResponseSerializer')
    def test_lists_single_post_successfully(self, mock_serializer):
        viewset = PostsViewSet()
        request = MagicMock()
        request.query_params = {'post_id': 1}
        post = MagicMock()
        viewset.get_object = MagicMock(return_value=post)
        serializer_instance = mock_serializer.return_value
        serializer_instance.data = {'id': 1, 'title': 'test'}

        response = viewset.list(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': 1, 'title': 'test'})
