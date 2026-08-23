from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.service_orders.serializers import (
    ServiceOrderInputSerializer,
    ServiceOrderSerializer,
)
from config.views import ErrorSerializer


class ServiceOrderCreateView(APIView):
    """Cria novas ordens de serviço para usuários autenticados."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        tags=["Ordens de Serviço"],
        summary="Criar ordem de serviço",
        description="Abre uma nova ordem de serviço para um equipamento pertencente ao cliente informado.",
        request=ServiceOrderInputSerializer,
        responses={
            201: ServiceOrderSerializer,
            400: ErrorSerializer,
            401: ErrorSerializer,
        },
        auth=[{"TokenAuth": []}],
    )
    def post(self, request, *args, **kwargs):
        serializer = ServiceOrderInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        service_order = serializer.save()
        return Response(
            ServiceOrderSerializer(service_order).data,
            status=status.HTTP_201_CREATED,
        )
