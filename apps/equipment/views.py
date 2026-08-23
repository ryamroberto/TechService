from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.equipment.models import Equipment
from apps.equipment.serializers import EquipmentInputSerializer, EquipmentSerializer
from config.views import ErrorSerializer


class EquipmentListCreateView(APIView):
    """Lista e cria equipamentos para usuários autenticados."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        tags=["Equipamentos"],
        summary="Listar equipamentos",
        parameters=[
            OpenApiParameter(
                name="customer_id",
                description="Filtro opcional pelo ID do cliente",
                required=False,
                type=int,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={
            200: EquipmentSerializer(many=True),
            401: ErrorSerializer,
        },
        auth=[{"TokenAuth": []}],
    )
    def get(self, request, *args, **kwargs):
        queryset = Equipment.objects.all().order_by("id")
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

        return Response(EquipmentSerializer(queryset, many=True).data)

    @extend_schema(
        tags=["Equipamentos"],
        summary="Criar equipamento",
        request=EquipmentInputSerializer,
        responses={
            201: EquipmentSerializer,
            400: ErrorSerializer,
            401: ErrorSerializer,
        },
        auth=[{"TokenAuth": []}],
    )
    def post(self, request, *args, **kwargs):
        serializer = EquipmentInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        equipment = serializer.save()
        return Response(
            EquipmentSerializer(equipment).data,
            status=status.HTTP_201_CREATED,
        )


class EquipmentDetailView(APIView):
    """Consulta e atualiza parcialmente um equipamento autenticado."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_equipment(self, pk):
        try:
            return Equipment.objects.get(pk=pk)
        except (Equipment.DoesNotExist, ValueError) as error:
            raise NotFound("Not found.") from error

    @extend_schema(
        tags=["Equipamentos"],
        summary="Consultar equipamento",
        responses={
            200: EquipmentSerializer,
            401: ErrorSerializer,
            404: ErrorSerializer,
        },
        auth=[{"TokenAuth": []}],
    )
    def get(self, request, pk, *args, **kwargs):
        equipment = self.get_equipment(pk)
        return Response(EquipmentSerializer(equipment).data)

    @extend_schema(
        tags=["Equipamentos"],
        summary="Atualizar equipamento",
        request=EquipmentInputSerializer,
        responses={
            200: EquipmentSerializer,
            400: ErrorSerializer,
            401: ErrorSerializer,
            404: ErrorSerializer,
        },
        auth=[{"TokenAuth": []}],
    )
    def patch(self, request, pk, *args, **kwargs):
        equipment = self.get_equipment(pk)
        serializer = EquipmentInputSerializer(
            equipment,
            data=request.data,
            partial=True,
        )
        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        equipment = serializer.save()
        return Response(EquipmentSerializer(equipment).data)
