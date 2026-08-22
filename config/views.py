"""
Views de configuração, saúde e autenticação da API.
"""

from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
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
        auth=[],
    )
    def get(self, request, *args, **kwargs):
        return Response(
            {
                "status": "ok",
                "service": "TechService API",
            },
            status=status.HTTP_200_OK,
        )


class TokenRequestSerializer(serializers.Serializer):
    """Dados necessários para autenticar um usuário local."""

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class TokenResponseSerializer(serializers.Serializer):
    """Resposta pública da emissão de token."""

    token = serializers.CharField(required=True)


class ErrorSerializer(serializers.Serializer):
    """Formato de erro utilizado pelo endpoint de autenticação."""

    detail = serializers.CharField(required=False)
    errors = serializers.DictField(required=False)


class TokenObtainView(APIView):
    """Emite um token para um usuário local com credenciais válidas."""

    permission_classes = (AllowAny,)
    authentication_classes = ()

    @extend_schema(
        tags=["Autenticação"],
        summary="Obter token de autenticação",
        request=TokenRequestSerializer,
        responses={
            200: TokenResponseSerializer,
            400: ErrorSerializer,
        },
        auth=[],
    )
    def post(self, request, *args, **kwargs):
        serializer = TokenRequestSerializer(data=request.data)
        if not serializer.is_valid():
            errors = {
                field: [str(message) for message in messages]
                for field, messages in serializer.errors.items()
            }
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            request=request,
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        if user is None:
            return Response(
                {"detail": "Credenciais inválidas."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key},
            status=status.HTTP_200_OK,
        )
