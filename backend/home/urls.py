from django.urls import include, path
from rest_framework.routers import DefaultRouter

from home.views import *

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'emission-scopes', EmissionScopeViewSet)
router.register(r'document-uploads', DocumentUploadViewSet)
router.register(r'emission-data', EmissionDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/captcha/', CaptchaView.as_view(), name='captcha'),
    path(
        'api/validate-captcha/',
        ValidateCaptchaView.as_view(),
        name='validate-captcha',
    ),
    path('auth_reset/', AuthResetView.as_view(), name='auth_reset'),
    path('auth_login/', AuthLoginView.as_view(), name='auth_login'),
    path(
        'change_password/',
        ChangePasswordView.as_view(),
        name='change_password',
    ),
    path('user/me/', UserDetail.as_view(), name='user-detail'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
