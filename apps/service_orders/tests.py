from django.contrib.auth import get_user_model
from django.db.models import ProtectedError
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.customers.models import Customer
from apps.equipment.models import Equipment
from apps.service_orders.models import ServiceOrder, ServiceOrderStatus


class ServiceOrderAPITests(APITestCase):
    """Testes automatizados da abertura e regras de negócio de ordens de serviço."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="atendente_os",
            password="senha-segura-123",
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

        # Clientes
        self.customer_1 = Customer.objects.create(
            name="Mariana Souza",
            phone="(11) 98888-1111",
            email="mariana@example.com",
        )
        self.customer_2 = Customer.objects.create(
            name="Roberto Ferreira",
            phone="(21) 97777-2222",
            email="roberto@example.com",
        )

        # Equipamentos
        self.equipment_1 = Equipment.objects.create(
            customer=self.customer_1,
            type="Celular",
            brand="Samsung",
            model="Galaxy S23",
            identifier="IMEI-987654321",
        )
        self.equipment_2 = Equipment.objects.create(
            customer=self.customer_2,
            type="Notebook",
            brand="Dell",
            model="Inspiron 15",
            identifier="TAG-12345",
        )

        self.valid_payload = {
            "customer_id": self.customer_1.id,
            "equipment_id": self.equipment_1.id,
            "problem_description": "Tela quebrada após impacto, sem touch.",
        }

    def test_create_service_order_success(self):
        """Cria uma ordem de serviço válida com status inicial recebido."""
        url = reverse("service-order-create")
        response = self.client.post(url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["customer_id"], self.customer_1.id)
        self.assertEqual(response.data["equipment_id"], self.equipment_1.id)
        self.assertEqual(
            response.data["problem_description"],
            "Tela quebrada após impacto, sem touch.",
        )
        self.assertEqual(response.data["status"], "recebido")
        self.assertIsNone(response.data["diagnosis"])
        self.assertIsNone(response.data["estimated_budget"])
        self.assertIsNone(response.data["notes"])
        self.assertIn("id", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)

        # Verifica persistência no banco
        self.assertTrue(
            ServiceOrder.objects.filter(
                id=response.data["id"],
                customer=self.customer_1,
                equipment=self.equipment_1,
                status=ServiceOrderStatus.RECEBIDO,
            ).exists()
        )

    def test_create_service_order_with_unrelated_equipment_fails(self):
        """Rejeita criação quando o equipamento pertence a outro cliente."""
        url = reverse("service-order-create")
        payload = {
            "customer_id": self.customer_1.id,
            "equipment_id": self.equipment_2.id,  # Pertence ao customer_2
            "problem_description": "Equipamento não liga.",
        }
        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)
        self.assertIn("equipment_id", response.data["errors"])
        self.assertEqual(
            response.data["errors"]["equipment_id"][0],
            "O equipamento informado não pertence ao cliente selecionado.",
        )
        self.assertFalse(
            ServiceOrder.objects.filter(
                customer=self.customer_1, equipment=self.equipment_2
            ).exists()
        )

    def test_create_service_order_nonexistent_customer_fails(self):
        """Rejeita criação quando o cliente informado não existe."""
        url = reverse("service-order-create")
        payload = {
            "customer_id": 999999,
            "equipment_id": self.equipment_1.id,
            "problem_description": "Bateria descarregando muito rápido.",
        }
        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)
        self.assertIn("customer_id", response.data["errors"])
        self.assertFalse(
            ServiceOrder.objects.filter(
                problem_description="Bateria descarregando muito rápido."
            ).exists()
        )

    def test_create_service_order_nonexistent_equipment_fails(self):
        """Rejeita criação quando o equipamento informado não existe."""
        url = reverse("service-order-create")
        payload = {
            "customer_id": self.customer_1.id,
            "equipment_id": 999999,
            "problem_description": "Teclado não responde.",
        }
        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)
        self.assertIn("equipment_id", response.data["errors"])
        self.assertFalse(
            ServiceOrder.objects.filter(
                problem_description="Teclado não responde."
            ).exists()
        )

    def test_create_service_order_missing_problem_description_fails(self):
        """Rejeita criação sem a descrição obrigatória do problema."""
        url = reverse("service-order-create")
        payload = {
            "customer_id": self.customer_1.id,
            "equipment_id": self.equipment_1.id,
            "problem_description": "   ",  # String vazia/apenas espaços
        }
        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)
        self.assertIn("problem_description", response.data["errors"])

    def test_create_service_order_missing_required_fields_fails(self):
        """Rejeita requisição com payload vazio."""
        url = reverse("service-order-create")
        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)
        self.assertIn("customer_id", response.data["errors"])
        self.assertIn("equipment_id", response.data["errors"])
        self.assertIn("problem_description", response.data["errors"])

    def test_unauthenticated_request_fails(self):
        """Rejeita requisição sem token com HTTP 401 Unauthorized."""
        self.client.credentials()  # Remove autenticação
        url = reverse("service-order-create")
        response = self.client.post(url, self.valid_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(ServiceOrder.objects.exists())

    def test_openapi_schema_contains_service_orders(self):
        """Valida que o schema OpenAPI documenta o endpoint e os schemas de ordens de serviço."""
        schema_url = reverse("schema")
        response = self.client.get(schema_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        schema_data = response.data
        self.assertIn("/api/service-orders/", schema_data["paths"])
        self.assertIn("ServiceOrder", schema_data["components"]["schemas"])
        self.assertIn("ServiceOrderInput", schema_data["components"]["schemas"])

    def test_service_order_str_representation(self):
        """Valida a representação em string do modelo ServiceOrder."""
        so = ServiceOrder.objects.create(
            customer=self.customer_1,
            equipment=self.equipment_1,
            problem_description="Falha de inicialização.",
            status=ServiceOrderStatus.RECEBIDO,
        )
        self.assertEqual(str(so), f"OS #{so.id} - Mariana Souza (Recebido)")

    def test_on_delete_protect_prevents_customer_and_equipment_deletion(self):
        """Valida que on_delete=models.PROTECT impede a deleção de clientes ou equipamentos com OS vinculada."""
        so = ServiceOrder.objects.create(
            customer=self.customer_1,
            equipment=self.equipment_1,
            problem_description="Troca de conector de carga.",
        )

        with self.assertRaises(ProtectedError):
            self.customer_1.delete()

        with self.assertRaises(ProtectedError):
            self.equipment_1.delete()

        self.assertTrue(ServiceOrder.objects.filter(id=so.id).exists())
