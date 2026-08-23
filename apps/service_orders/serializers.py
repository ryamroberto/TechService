from decimal import Decimal

from rest_framework import serializers

from apps.customers.models import Customer
from apps.equipment.models import Equipment
from apps.service_orders.models import ServiceOrder, ServiceOrderStatus


class ServiceOrderInputSerializer(serializers.ModelSerializer):
    """Valida os dados aceitos na criação de ordens de serviço."""

    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source="customer",
        error_messages={
            "does_not_exist": "Cliente informado não foi encontrado ou não existe.",
            "incorrect_type": "Identificador de cliente inválido.",
        },
    )
    equipment_id = serializers.PrimaryKeyRelatedField(
        queryset=Equipment.objects.all(),
        source="equipment",
        error_messages={
            "does_not_exist": "Equipamento informado não foi encontrado ou não existe.",
            "incorrect_type": "Identificador de equipamento inválido.",
        },
    )
    problem_description = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "blank": "A descrição do problema é obrigatória.",
            "required": "A descrição do problema é obrigatória.",
        },
    )

    class Meta:
        model = ServiceOrder
        fields = ("customer_id", "equipment_id", "problem_description")

    def validate_problem_description(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("A descrição do problema é obrigatória.")
        return value.strip()

    def validate(self, attrs):
        customer = attrs.get("customer")
        equipment = attrs.get("equipment")

        if customer and equipment and equipment.customer_id != customer.id:
            raise serializers.ValidationError(
                {
                    "equipment_id": [
                        "O equipamento informado não pertence ao cliente selecionado."
                    ]
                }
            )

        return attrs

    def create(self, validated_data):
        # Abertura sempre inicializa com status 'recebido'
        validated_data["status"] = ServiceOrderStatus.RECEBIDO
        return super().create(validated_data)


class ServiceOrderUpdateInputSerializer(serializers.ModelSerializer):
    """Valida os dados aceitos na atualização parcial de ordens de serviço."""

    status = serializers.ChoiceField(
        choices=ServiceOrderStatus.choices,
        required=False,
        error_messages={
            "invalid_choice": "Status informado é inválido.",
        },
    )
    diagnosis = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )
    estimated_budget = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        allow_null=True,
        min_value=Decimal("0.00"),
        error_messages={
            "min_value": "O orçamento estimado não pode ser negativo.",
            "invalid": "O orçamento estimado deve ser um valor numérico válido.",
        },
    )
    notes = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )

    class Meta:
        model = ServiceOrder
        fields = ("status", "diagnosis", "estimated_budget", "notes")


class ServiceOrderSerializer(serializers.ModelSerializer):
    """Representa uma ordem de serviço nas respostas da API."""

    customer_id = serializers.IntegerField(read_only=True)
    equipment_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ServiceOrder
        fields = (
            "id",
            "customer_id",
            "equipment_id",
            "problem_description",
            "status",
            "diagnosis",
            "estimated_budget",
            "notes",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "customer_id",
            "equipment_id",
            "problem_description",
            "status",
            "diagnosis",
            "estimated_budget",
            "notes",
            "created_at",
            "updated_at",
        )
