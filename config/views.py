"""
Views de configuração e saúde da API.
"""

from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthResponseSerializer(serializers.Serializer):
    """Schema para a resposta do endpoint de verificação de saúde."""

    status = serializers.CharField(
        required=True,
        help_text="Status operacional da aplicação (ex: ok)",
    )
    service = serializers.CharField(
        required=True,
        help_text="Nome do serviço (ex: TechService API)",
    )


class HealthCheckView(APIView):
    """
    Endpoint público para verificação da disponibilidade da API.
    """

    permission_classes = (AllowAny,)
    authentication_classes = ()

    @extend_schema(
        tags=["Saúde"],
        summary="Verificar disponibilidade da API",
        description="Retorna o status operacional da aplicação e o nome do serviço.",
        responses={200: HealthResponseSerializer},
    )
    def get(self, request, *args, **kwargs):
        return Response(
            {
                "status": "ok",
                "service": "TechService API",
            },
            status=status.HTTP_200_OK,
        )
