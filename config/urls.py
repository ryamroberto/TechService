"""
URL configuration for TechService project.
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from config.views import HealthCheckView, TokenObtainView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Rota pública de saúde
    path("api/health/", HealthCheckView.as_view(), name="health-check"),
    # Rota pública para obtenção de token
    path("api/auth/token/", TokenObtainView.as_view(), name="api-token-auth"),
    # Rotas protegidas de clientes
    path("api/customers/", include("apps.customers.urls")),
    # Rotas protegidas de equipamentos
    path("api/equipment/", include("apps.equipment.urls")),
    # Documentação OpenAPI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
]
