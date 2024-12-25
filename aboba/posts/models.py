import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation,
)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from rest_framework.exceptions import ValidationError


class Post(models.Model):
    post_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    file_type = models.CharField(
        max_length=10,
        choices=[('image', 'Image'), ('video', 'Video')],
    )
    file_key = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    comments = GenericRelation('Comments')

    def __str__(self):
        return f'Post {self.post_id} - {self.file_type}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Comments(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    parent_comment = models.ForeignKey(
        to='self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
    )

    def __str__(self):
        return f'{self.content_object}'

    def clean(self):
        if self.parent_comment and self.content_type.model != 'comments':
            raise ValidationError('Parent comment must reference another comment.')
        if not self.parent_comment and self.content_type.model != 'post':
            raise ValidationError('Top-level comments must reference a post.')

    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['parent_comment']),
        ]
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
