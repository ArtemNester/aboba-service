import uuid

from config import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from utils import (
    send_event_to_broker,
    upload_media_to_s3,
)

from .models import (
    Comments,
    Post,
)


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CommentRequestSerializer(serializers.Serializer):
    post_id = serializers.UUIDField(required=False)
    parent_comment_id = serializers.UUIDField(required=False)
    content = serializers.CharField(required=True)

    def validate(self, attrs):
        post_id = attrs.get('post_id')
        parent_comment_id = attrs.get('parent_comment_id')

        if post_id and parent_comment_id:
            raise serializers.ValidationError(
                'You can only provide either post_id or parent_comment_id, not both.',
            )

        if not post_id and not parent_comment_id:
            raise serializers.ValidationError(
                'You must provide either post_id or parent_comment_id.',
            )

        return attrs

    def create(self, validated_data):
        request = self.context['request']
        content = validated_data['content']
        parent_comment_id = validated_data.get('parent_comment_id')
        post_id = validated_data.get('post_id')

        if parent_comment_id:
            try:
                parent_comment = Comments.objects.get(id=parent_comment_id)
            except Comments.DoesNotExist:
                raise serializers.ValidationError(
                    'parent_comment_id: Parent comment does not exist',
                )

            comment = Comments(
                content=content,
                content_object=parent_comment.content_object,
                user=request.user,
                parent_comment=parent_comment,
            )
        elif post_id:
            try:
                post = Post.objects.get(post_id=post_id)
            except Post.DoesNotExist:
                raise serializers.ValidationError('post_id: Post does not exist')

            comment = Comments(
                content=content,
                content_object=post,
                user=request.user,
            )
        else:
            raise serializers.ValidationError('Post or parent comment must be provided')

        comment.save()
        return comment


class CommentResponseSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comments
        fields = ['id', 'content', 'created_at', 'user', 'parent_comment_id']


class PostResponseSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    post_comments = CommentResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'post_id',
            'file_type',
            'file_key',
            'created_at',
            'user',
            'post_comments',
        ]


class UploadPostRequestSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)
    file_type = serializers.ChoiceField(choices=['image', 'video'], required=True)

    def create(self, validated_data):
        request = self.context['request']
        file = validated_data['file']
        file_type = validated_data['file_type']

        file_key = f'{uuid.uuid4()}_{file.name}'

        upload_media_to_s3(
            bucket_name=settings.MINIO_BUCKET_NAME,
            file_key=file_key,
            file=file,
            file_size=file.size,
        )

        event_data = {
            'notification_upload_user_id': request.user.id,
            'notification_upload_file_key': file_key,
        }

        post = Post.objects.create(
            user=request.user,
            file_type=file_type,
            file_key=file_key,
        )

        transaction.on_commit(lambda: send_event_to_broker(event_data=event_data))

        return post


class UploadPostResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['post_id', 'file_key', 'file_type', 'created_at']
