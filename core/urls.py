from django.contrib import admin
from django.urls import path, include, re_path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import yaml


schema_view = get_schema_view(
    openapi.Info(
        title="Chess Tournament System API",
        default_version='v1',
        description='API for managing chess tournaments and players'
    ),
    public=True
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/', include('tournaments.urls')),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]