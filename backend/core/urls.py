from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from rest_framework_simplejwt import views as jwt_views

schema_view = get_schema_view(
    openapi.Info(
        title='Snippets API',
        default_version='v1',
        description='Api Consignados',
        terms_of_service='',
        contact=openapi.Contact(email=''),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

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
    path(
        'swagger/<format>',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)