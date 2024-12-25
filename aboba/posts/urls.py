from rest_framework.routers import DefaultRouter

from .views import (
    CommentsViewSet,
    PostsViewSet,
    UploadMemeMemeViewSet,
)


router = DefaultRouter()

router.register(r'upload', UploadMemeMemeViewSet, basename='upload_meme')
router.register(r'', PostsViewSet, basename='posts')
router.register(r'create/comment', CommentsViewSet, basename='comments')

urlpatterns = router.urls
