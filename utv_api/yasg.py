from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



shema_view = get_schema_view(
    openapi.Info(
        title="Utv smeta",
        default_version='v1',
        description='Test api utv smeta',
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger(?P<format>\.json|\.yaml)', shema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', shema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', shema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]