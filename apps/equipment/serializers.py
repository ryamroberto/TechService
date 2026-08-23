from rest_framework import serializers

from apps.customers.models import Customer
from apps.equipment.models import Equipment


class EquipmentInputSerializer(serializers.ModelSerializer):
    """Valida os dados aceitos na criação e atualização de equipamentos."""

    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source="customer",
        error_messages={
            "does_not_exist": "Cliente informado não foi encontrado ou não existe.",
            "incorrect_type": "Identificador de cliente inválido.",
        },
    )

    class Meta:
        model = Equipment
        fields = ("customer_id", "type", "brand", "model", "identifier")


class EquipmentSerializer(serializers.ModelSerializer):
    """Representa um equipamento nas respostas da API."""

    customer_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Equipment
        fields = (
            "id",
            "customer_id",
            "type",
            "brand",
            "model",
            "identifier",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "customer_id", "created_at", "updated_at")
