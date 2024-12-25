import unittest
from unittest.mock import (
    MagicMock,
    patch,
)

from posts.serializers import CommentResponseSerializer
from posts.views import CommentsViewSet
from rest_framework import status
from rest_framework.exceptions import ValidationError


class CommentsViewSetTests(unittest.TestCase):
    @patch('posts.views.CommentRequestSerializer')
    def test_creates_comment_successfully(self, mock_serializer):
        viewset = CommentsViewSet()
        request = MagicMock()
        request.data = {'text': 'test comment'}
        serializer_instance = mock_serializer.return_value
        serializer_instance.is_valid.return_value = True
        comment = MagicMock()
        serializer_instance.save.return_value = comment
        response_serializer = MagicMock()
        response_serializer.data = {'id': 1, 'text': 'test comment'}
        CommentResponseSerializer.return_value = response_serializer

        response = viewset.create(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'id': 1, 'text': 'test comment'})

    @patch('posts.views.CommentRequestSerializer')
    def test_handles_validation_error(self, mock_serializer):
        viewset = CommentsViewSet()
        request = MagicMock()
        request.data = {'text': ''}
        serializer_instance = mock_serializer.return_value
        serializer_instance.is_valid.side_effect = ValidationError('Invalid data')

        response = viewset.create(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors_create', response.data)
