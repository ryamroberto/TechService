"""
Testes automatizados para configuração e rota de saúde.
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class HealthCheckTests(APITestCase):
    """Testes da rota de verificação de saúde da API."""

    def test_health_check_returns_200_and_expected_payload(self):
        """Valida que a rota /api/health/ responde 200 OK com payload esperado."""
        url = reverse("health-check")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "status": "ok",
                "service": "TechService API",
            },
        )

    def test_health_check_is_public_without_authentication(self):
        """Valida que a rota /api/health/ é pública e não exige token de autenticação."""
        self.client.credentials()  # Sem credenciais no header
        response = self.client.get("/api/health/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("status"), "ok")
        self.assertEqual(response.data.get("service"), "TechService API")
