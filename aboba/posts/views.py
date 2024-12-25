from django.contrib.contenttypes.models import ContentType
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import (
    status,
    viewsets,
)
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    Comments,
    Post,
)
from .pagination import PostPagination
from .serializers import (
    CommentRequestSerializer,
    CommentResponseSerializer,
    PostResponseSerializer,
    UploadPostRequestSerializer,
    UploadPostResponseSerializer,
)


class UploadMemeMemeViewSet(viewsets.ModelViewSet):
    serializer_class = UploadPostRequestSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        response_serializer = UploadPostResponseSerializer(data)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class PostsViewSet(viewsets.ModelViewSet):
    queryset = (
        Post.objects.prefetch_related(
            Prefetch(
                'comments',
                queryset=Comments.objects.all(),
                to_attr='post_comments',
            ),
        )
        .all()
        .order_by('-created_at')
    )

    serializer_class = PostResponseSerializer
    pagination_class = PostPagination
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        post_id = request.query_params.get('post_id')
        if post_id:
            post = get_object_or_404(self.queryset, post_id=post_id)
            serializer = self.get_serializer(post)
            return Response(serializer.data)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentRequestSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            comment = serializer.save()
            response_serializer = CommentResponseSerializer(comment)
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED,
            )
        except ValidationError as e:
            return Response(
                data={'errors_create': e.get_full_details()},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def list(self, request, *args, **kwargs):
        post_id = request.query_params.get('post_id')
        parent_comment_id = request.query_params.get('parent_comment_id')

        if post_id:
            comments = Comments.objects.filter(
                content_type=ContentType.objects.get_for_model(Post),
                object_id=post_id,
                parent_comment__isnull=True,
            )
        elif parent_comment_id:
            comments = Comments.objects.filter(parent_comment_id=parent_comment_id)
        else:
            comments = Comments.objects.none()
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)
