import unittest
from unittest.mock import (
    MagicMock,
    patch,
)

from posts.serializers import UploadPostResponseSerializer
from posts.views import UploadMemeMemeViewSet
from rest_framework import status
from rest_framework.exceptions import ValidationError


class UploadMemeMemeViewSetTests(unittest.TestCase):
    @patch('posts.views.UploadPostRequestSerializer')
    def test_creates_meme_successfully(self, mock_serializer):
        viewset = UploadMemeMemeViewSet()
        request = MagicMock()
        request.data = {'file': 'test_file'}
        serializer_instance = mock_serializer.return_value
        serializer_instance.is_valid.return_value = True
        serializer_instance.save.return_value = {
            'file_key': 'key',
            'file_type': 'type',
            'created_at': 'now',
        }
        response_serializer = MagicMock()
        response_serializer.data = {
            'file_key': 'key',
            'file_type': 'type',
            'created_at': 'now',
        }
        UploadPostResponseSerializer.return_value = response_serializer

        response = viewset.create(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            {'file_key': 'key', 'file_type': 'type', 'created_at': 'now'},
        )

    @patch('posts.views.UploadPostRequestSerializer')
    def test_handles_validation_error(self, mock_serializer):
        viewset = UploadMemeMemeViewSet()
        request = MagicMock()
        request.data = {'file': ''}
        serializer_instance = mock_serializer.return_value
        serializer_instance.is_valid.side_effect = ValidationError('Invalid data')

        response = viewset.create(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors_create', response.data)
