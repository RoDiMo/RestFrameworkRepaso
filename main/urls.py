from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from main import views

router = DefaultRouter()
router.register(r'marca', views.MarcaViewSet, basename='marca')
router.register(r'vehiculo', views.VehiculoViewSet, basename='vehiculo')

# Ejercicio 2
router.register(r'patinetes', views.PatineteviewSet, basename='patinete')
router.register(r'usuarios', views.UsuarioViewSet, basename='usuario')
router.register(r'alquileres', views.AlquilerViewSet, basename='alquiler')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('openapi', get_schema_view(
        title="Your Project",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='main/swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
]
