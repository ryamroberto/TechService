from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.service_orders.models import ServiceOrder, ServiceOrderStatus
from apps.service_orders.serializers import (
    ServiceOrderInputSerializer,
    ServiceOrderSerializer,
    ServiceOrderUpdateInputSerializer,
)
from config.views import ErrorSerializer


class ServiceOrderListCreateView(APIView):
    """Lista e cria ordens de serviço para usuários autenticados."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        tags=["Ordens de Serviço"],
        summary="Listar ordens de serviço",
        description="Lista todas as ordens de serviço com suporte a filtros opcionais por cliente e por status.",
        parameters=[
            OpenApiParameter(
                name="customer_id",
                description="Filtro opcional pelo ID do cliente",
                required=False,
                type=int,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="status",
                description="Filtro opcional pelo status da ordem",
                required=False,
                type=str,
                enum=ServiceOrderStatus.values,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={
            200: ServiceOrderSerializer(many=True),
            400: ErrorSerializer,
            401: ErrorSerializer,
        },
        auth=[{"TokenAuth": []}],
    )
    def get(self, request, *args, **kwargs):
        queryset = ServiceOrder.objects.all().order_by("-created_at", "-id")

        customer_id = request.query_params.get("customer_id")
        if customer_id is not None and customer_id != "":
            try:
                customer_id_int = int(customer_id)
                queryset = queryset.filter(customer_id=customer_id_int)
            except ValueError:
                return Response(
                    {
                        "errors": {
                            "customer_id": [
                                "O parâmetro customer_id deve ser um número inteiro válido."
                            ]
                        }
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        status_param = request.query_params.get("status")
        if status_param is not None and status_param != "":
            if status_param not in ServiceOrderStatus.values:
                return Response(
                    {
                        "errors": {
                            "status": [
                                f"Status '{status_param}' é inválido. Opções permitidas: {', '.join(ServiceOrderStatus.values)}."
                            ]
                        }
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            queryset = queryset.filter(status=status_param)

        return Response(ServiceOrderSerializer(queryset, many=True).data)

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


# Alias para compatibilidade
ServiceOrderCreateView = ServiceOrderListCreateView


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
        summary="Consultar ordem de serviço",
        description="Consulta os dados detalhados de uma ordem de serviço existente.",
        responses={
            200: ServiceOrderSerializer,
            401: ErrorSerializer,
            404: ErrorSerializer,
        },
        auth=[{"TokenAuth": []}],
    )
    def get(self, request, pk, *args, **kwargs):
        service_order = self.get_service_order(pk)
        return Response(ServiceOrderSerializer(service_order).data)

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
