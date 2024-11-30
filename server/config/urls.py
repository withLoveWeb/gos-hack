from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.permissions import AllowAny

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v1',
   ),
   public=True,
   permission_classes = [AllowAny], 
   authentication_classes = []

)

urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),

    path('user/', include('user.urls')),
    path('route/', include('route.urls')),
    path('captain/', include('captain.urls')),
]

