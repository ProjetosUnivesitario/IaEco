from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from rest_framework_simplejwt import views as jwt_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
    path(
        'api/v1/token/',
        jwt_views.TokenObtainPairView.as_view(),
        name='token_obtain_pair',
    ),
    path(
        'api/v1/token/refresh/',
        jwt_views.TokenRefreshView.as_view(),
        name='token_refresh',
    ),
    path(
        'api/v1/token/verify/',
        jwt_views.TokenVerifyView.as_view(),
        name='token_verify',
    ),
    path('api/v1/', include('home.urls')),
    path('captcha/', include('captcha.urls')),
    path('__debug__/', include('debug_toolbar.urls')),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [
      path('__debug__/', include('debug_toolbar.urls')),  
    ]
