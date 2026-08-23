from rest_framework import serializers

from apps.customers.models import Customer


class CustomerInputSerializer(serializers.ModelSerializer):
    """Valida os dados aceitos na criação e atualização de clientes."""

    class Meta:
        model = Customer
        fields = ("name", "phone", "email")


class CustomerSerializer(serializers.ModelSerializer):
    """Representa um cliente nas respostas da API."""

    class Meta:
        model = Customer
        fields = (
            "id",
            "name",
            "phone",
            "email",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
