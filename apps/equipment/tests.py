from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.customers.models import Customer
from apps.equipment.models import Equipment


class EquipmentAPITests(APITestCase):
    """Testes automatizados do domínio de equipamentos."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="atendente_equip",
            password="senha-segura-123",
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        self.customer = Customer.objects.create(
            name="Carlos Oliveira",
            phone="(11) 98888-7777",
            email="carlos@example.com",
        )
        self.customer_2 = Customer.objects.create(
            name="Ana Santos",
            phone="(21) 97777-6666",
            email="ana@example.com",
        )

        self.valid_payload = {
            "customer_id": self.customer.id,
            "type": "Celular",
            "brand": "Samsung",
            "model": "Galaxy A54",
            "identifier": "IMEI-123456789",
        }

    def test_create_equipment_success(self):
        """Cria equipamento com sucesso para cliente existente."""
        url = reverse("equipment-list-create")
        response = self.client.post(url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["customer_id"], self.customer.id)
        self.assertEqual(response.data["type"], "Celular")
        self.assertEqual(response.data["brand"], "Samsung")
        self.assertEqual(response.data["model"], "Galaxy A54")
        self.assertEqual(response.data["identifier"], "IMEI-123456789")
        self.assertIn("id", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)
        self.assertTrue(Equipment.objects.filter(id=response.data["id"]).exists())

    def test_create_equipment_without_identifier_success(self):
        """Cria equipamento sem identifier (campo opcional)."""
        url = reverse("equipment-list-create")
        payload = {
            "customer_id": self.customer.id,
            "type": "Computador",
            "brand": "Dell",
            "model": "OptiPlex 3080",
        }
        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data["identifier"])
        self.assertEqual(response.data["brand"], "Dell")

    def test_create_equipment_missing_required_fields_fails(self):
        """Rejeita criação de equipamento com campos obrigatórios ausentes."""
        url = reverse("equipment-list-create")
        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)
        self.assertIn("customer_id", response.data["errors"])
        self.assertIn("type", response.data["errors"])
        self.assertIn("brand", response.data["errors"])
        self.assertIn("model", response.data["errors"])

    def test_create_equipment_nonexistent_customer_fails(self):
        """Rejeita criação de equipamento quando customer_id não existe."""
        url = reverse("equipment-list-create")
        payload = {
            "customer_id": 999999,
            "type": "Impressora",
            "brand": "Epson",
            "model": "EcoTank L3250",
        }
        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)
        self.assertIn("customer_id", response.data["errors"])
        self.assertFalse(Equipment.objects.filter(brand="Epson").exists())

    def test_list_all_equipment_success(self):
        """Lista todos os equipamentos cadastrados."""
        Equipment.objects.create(
            customer=self.customer,
            type="Celular",
            brand="Apple",
            model="iPhone 13",
        )
        Equipment.objects.create(
            customer=self.customer_2,
            type="Notebook",
            brand="Lenovo",
            model="ThinkPad E14",
        )

        url = reverse("equipment-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)

    def test_list_equipment_filter_by_customer_id_success(self):
        """Filtra equipamentos pelo parâmetro opcional customer_id."""
        eq1 = Equipment.objects.create(
            customer=self.customer,
            type="Celular",
            brand="Apple",
            model="iPhone 13",
        )
        Equipment.objects.create(
            customer=self.customer_2,
            type="Notebook",
            brand="Lenovo",
            model="ThinkPad E14",
        )

        url = reverse("equipment-list-create")
        response = self.client.get(url, {"customer_id": self.customer.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], eq1.id)
        self.assertEqual(response.data[0]["customer_id"], self.customer.id)

    def test_retrieve_equipment_success(self):
        """Consulta detalhes de um equipamento específico por ID."""
        equipment = Equipment.objects.create(
            customer=self.customer,
            type="Celular",
            brand="Motorola",
            model="Moto G84",
            identifier="SN987654",
        )

        url = reverse("equipment-detail", kwargs={"pk": equipment.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], equipment.id)
        self.assertEqual(response.data["brand"], "Motorola")
        self.assertEqual(response.data["identifier"], "SN987654")

    def test_retrieve_nonexistent_equipment_returns_404(self):
        """Retorna HTTP 404 Not Found para equipamento inexistente."""
        url = reverse("equipment-detail", kwargs={"pk": 999999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"detail": "Not found."})

    def test_partial_update_equipment_success(self):
        """Atualiza parcialmente os dados de um equipamento com PATCH."""
        equipment = Equipment.objects.create(
            customer=self.customer,
            type="Celular",
            brand="Xiaomi",
            model="Redmi Note 12",
        )

        url = reverse("equipment-detail", kwargs={"pk": equipment.id})
        response = self.client.patch(
            url,
            {"model": "Redmi Note 12 Pro", "identifier": "SN-NEW-123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["model"], "Redmi Note 12 Pro")
        self.assertEqual(response.data["identifier"], "SN-NEW-123")
        self.assertEqual(response.data["brand"], "Xiaomi")

    def test_partial_update_equipment_with_invalid_customer_fails(self):
        """Rejeita atualização parcial vinculando a cliente inexistente."""
        equipment = Equipment.objects.create(
            customer=self.customer,
            type="Tablet",
            brand="Samsung",
            model="Galaxy Tab A9",
        )

        url = reverse("equipment-detail", kwargs={"pk": equipment.id})
        response = self.client.patch(
            url,
            {"customer_id": 999999},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)
        self.assertIn("customer_id", response.data["errors"])

    def test_unauthenticated_requests_are_rejected(self):
        """Rejeita requisições sem token em todas as rotas de equipamentos."""
        self.client.credentials()  # Remove credenciais

        list_url = reverse("equipment-list-create")
        detail_url = reverse("equipment-detail", kwargs={"pk": 1})

        self.assertEqual(
            self.client.get(list_url).status_code, status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(
            self.client.post(list_url, self.valid_payload).status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.assertEqual(
            self.client.get(detail_url).status_code, status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(
            self.client.patch(detail_url, {"brand": "X"}).status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_openapi_schema_contains_equipment_endpoints(self):
        """Valida que o schema OpenAPI documenta as rotas de equipamentos."""
        schema_url = reverse("schema")
        response = self.client.get(schema_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        schema_data = response.data
        self.assertIn("/api/equipment/", schema_data["paths"])
        self.assertIn("/api/equipment/{id}/", schema_data["paths"])
        self.assertIn("Equipment", schema_data["components"]["schemas"])
        self.assertIn("EquipmentInput", schema_data["components"]["schemas"])
