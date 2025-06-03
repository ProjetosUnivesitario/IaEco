from django.urls import include, path
from rest_framework.routers import DefaultRouter

from home.views import (AuthLoginView, AuthResetView, CaptchaView,
                        ChangePasswordView, UserDetail, ValidateCaptchaView,
                        DocumentUploadView,
                        dashboard_data,
                        document_status)

router = DefaultRouter()


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
    path('upload/', DocumentUploadView.as_view(), name='document-upload'),
    path('dashboard/', dashboard_data, name='dashboard-data'),
    path('document/<uuid:document_id>/status/', document_status, name='document-status'),
]
