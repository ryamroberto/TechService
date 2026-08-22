"""
Testes automatizados para configuração, saúde e autenticação da API.
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
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


class TokenAuthenticationTests(APITestCase):
    """Testes do fluxo de autenticação por token."""

    def setUp(self):
        self.username = "atendente"
        self.password = "senha-segura-123"
        self.user = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
        )
        self.url = reverse("api-token-auth")

    def test_valid_credentials_return_token(self):
        """Credenciais válidas retornam 200 e persistem um token."""
        response = self.client.post(
            self.url,
            {"username": self.username, "password": self.password},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data.get("token"), str)
        self.assertTrue(response.data["token"])
        self.assertTrue(Token.objects.filter(user=self.user).exists())
        self.assertEqual(set(response.data), {"token"})

    def test_invalid_credentials_return_consistent_json_error(self):
        """Credenciais inválidas retornam erro JSON sem criar token."""
        response = self.client.post(
            self.url,
            {"username": self.username, "password": "senha-incorreta"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"detail": "Credenciais inválidas."})
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_missing_credentials_return_field_errors(self):
        """Payload sem campos obrigatórios retorna erros de validação em JSON."""
        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)
        self.assertIn("username", response.data["errors"])
        self.assertIn("password", response.data["errors"])

    def test_password_is_hashed_and_never_returned(self):
        """A senha não é armazenada em texto puro nem aparece na resposta."""
        response = self.client.post(
            self.url,
            {"username": self.username, "password": self.password},
            format="json",
        )

        self.user.refresh_from_db()
        self.assertNotEqual(self.user.password, self.password)
        self.assertNotIn("password", response.data)
        self.assertNotIn(self.password, response.content.decode())

    def test_health_remains_public_without_token(self):
        """A rota de saúde continua pública após ativar a autenticação padrão."""
        response = self.client.get(reverse("health-check"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "ok")
