from rest_framework.routers import DefaultRouter

from .views import (
    LoginViewSet,
    LogoutViewSet,
    RegisterViewSet,
)


router = DefaultRouter()

router.register(r'register', RegisterViewSet, basename='register')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'logout', LogoutViewSet, basename='logout')


urlpatterns = router.urls
