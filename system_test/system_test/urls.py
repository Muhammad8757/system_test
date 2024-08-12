from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from system_test_app.views import ActionAPIView, ActivateAPIView, SubjectAPIView, ThemeAPIView, UserAPIView, TestAPIView

router = DefaultRouter()
router.register(r'users', UserAPIView, basename='user')
router.register(r'subject', SubjectAPIView, basename='subject')
router.register(r'theme', ThemeAPIView, basename='theme')
router.register(r'test', TestAPIView, basename='test')
router.register(r'activate', ActivateAPIView, basename='activate')
router.register(r'action', ActionAPIView, basename='action')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]