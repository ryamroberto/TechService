from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.customers.models import Customer
from apps.customers.serializers import CustomerInputSerializer, CustomerSerializer
from config.views import ErrorSerializer


class CustomerListCreateView(APIView):
    """Lista e cria clientes para usuários autenticados."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        tags=["Clientes"],
        summary="Listar clientes",
        responses={
            200: CustomerSerializer(many=True),
            401: ErrorSerializer,
        },
        auth=[{"TokenAuth": []}],
    )
    def get(self, request, *args, **kwargs):
        customers = Customer.objects.all().order_by("id")
        return Response(CustomerSerializer(customers, many=True).data)

    @extend_schema(
        tags=["Clientes"],
        summary="Criar cliente",
        request=CustomerInputSerializer,
        responses={
            201: CustomerSerializer,
            400: ErrorSerializer,
            401: ErrorSerializer,
        },
        auth=[{"TokenAuth": []}],
    )
    def post(self, request, *args, **kwargs):
        serializer = CustomerInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        customer = serializer.save()
        return Response(
            CustomerSerializer(customer).data,
            status=status.HTTP_201_CREATED,
        )


class CustomerDetailView(APIView):
    """Consulta e atualiza parcialmente um cliente autenticado."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_customer(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist as error:
            raise NotFound("Not found.") from error

    @extend_schema(
        tags=["Clientes"],
        summary="Consultar cliente",
        responses={
            200: CustomerSerializer,
            401: ErrorSerializer,
            404: ErrorSerializer,
        },
        auth=[{"TokenAuth": []}],
    )
    def get(self, request, pk, *args, **kwargs):
        customer = self.get_customer(pk)
        return Response(CustomerSerializer(customer).data)

    @extend_schema(
        tags=["Clientes"],
        summary="Atualizar cliente",
        request=CustomerInputSerializer,
        responses={
            200: CustomerSerializer,
            400: ErrorSerializer,
            401: ErrorSerializer,
            404: ErrorSerializer,
        },
        auth=[{"TokenAuth": []}],
    )
    def patch(self, request, pk, *args, **kwargs):
        customer = self.get_customer(pk)
        serializer = CustomerInputSerializer(
            customer,
            data=request.data,
            partial=True,
        )
        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        customer = serializer.save()
        return Response(CustomerSerializer(customer).data)
