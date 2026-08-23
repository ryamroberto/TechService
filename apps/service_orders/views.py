from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.service_orders.models import ServiceOrder
from apps.service_orders.serializers import (
    ServiceOrderInputSerializer,
    ServiceOrderSerializer,
    ServiceOrderUpdateInputSerializer,
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


class ServiceOrderDetailView(APIView):
    """Consulta e atualiza parcialmente uma ordem de serviço autenticada."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_service_order(self, pk):
        try:
            return ServiceOrder.objects.get(pk=pk)
        except (ServiceOrder.DoesNotExist, ValueError) as error:
            raise NotFound("Not found.") from error

    @extend_schema(
        tags=["Ordens de Serviço"],
        summary="Atualizar ordem de serviço",
        description="Atualiza parcialmente o diagnóstico, orçamento estimado, observações e status da ordem de serviço.",
        request=ServiceOrderUpdateInputSerializer,
        responses={
            200: ServiceOrderSerializer,
            400: ErrorSerializer,
            401: ErrorSerializer,
            404: ErrorSerializer,
        },
        auth=[{"TokenAuth": []}],
    )
    def patch(self, request, pk, *args, **kwargs):
        service_order = self.get_service_order(pk)
        serializer = ServiceOrderUpdateInputSerializer(
            service_order,
            data=request.data,
            partial=True,
        )
        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        service_order = serializer.save()
        return Response(
            ServiceOrderSerializer(service_order).data,
            status=status.HTTP_200_OK,
        )
