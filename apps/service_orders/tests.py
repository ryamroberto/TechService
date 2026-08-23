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
        self.assertIn("ServiceOrderStatus", schema_data["components"]["schemas"])

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

    def test_update_service_order_all_fields_success(self):
        """Atualiza com sucesso diagnóstico, orçamento estimado, observações e status da ordem."""
        so = ServiceOrder.objects.create(
            customer=self.customer_1,
            equipment=self.equipment_1,
            problem_description="Aparelho reiniciando sozinho.",
            status=ServiceOrderStatus.RECEBIDO,
        )
        url = reverse("service-order-detail", kwargs={"pk": so.id})
        payload = {
            "status": "em_diagnostico",
            "diagnosis": "Curto-circuito na placa lógica principal.",
            "estimated_budget": "350.50",
            "notes": "Cliente informou que aparelho molhou na chuva.",
        }
        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], so.id)
        self.assertEqual(response.data["customer_id"], self.customer_1.id)
        self.assertEqual(response.data["equipment_id"], self.equipment_1.id)
        self.assertEqual(
            response.data["problem_description"], "Aparelho reiniciando sozinho."
        )
        self.assertEqual(response.data["status"], "em_diagnostico")
        self.assertEqual(
            response.data["diagnosis"], "Curto-circuito na placa lógica principal."
        )
        self.assertEqual(response.data["estimated_budget"], "350.50")
        self.assertEqual(
            response.data["notes"], "Cliente informou que aparelho molhou na chuva."
        )

        # Valida persistência no banco
        so.refresh_from_db()
        self.assertEqual(so.status, ServiceOrderStatus.EM_DIAGNOSTICO)
        self.assertEqual(so.diagnosis, "Curto-circuito na placa lógica principal.")
        self.assertEqual(str(so.estimated_budget), "350.50")
        self.assertEqual(so.notes, "Cliente informou que aparelho molhou na chuva.")

    def test_update_service_order_single_field_success(self):
        """Atualiza parcialmente apenas um campo sem alterar os outros."""
        so = ServiceOrder.objects.create(
            customer=self.customer_1,
            equipment=self.equipment_1,
            problem_description="Sem som no alto-falante.",
            status=ServiceOrderStatus.EM_DIAGNOSTICO,
            diagnosis="Alto-falante danificado.",
            estimated_budget="120.00",
            notes="Aguardando peça de reposição.",
        )
        url = reverse("service-order-detail", kwargs={"pk": so.id})
        response = self.client.patch(url, {"status": "em_conserto"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "em_conserto")
        self.assertEqual(response.data["diagnosis"], "Alto-falante danificado.")
        self.assertEqual(response.data["estimated_budget"], "120.00")
        self.assertEqual(response.data["notes"], "Aguardando peça de reposição.")

        so.refresh_from_db()
        self.assertEqual(so.status, ServiceOrderStatus.EM_CONSERTO)
        self.assertEqual(so.diagnosis, "Alto-falante danificado.")
        self.assertEqual(str(so.estimated_budget), "120.00")
        self.assertEqual(so.notes, "Aguardando peça de reposição.")

    def test_update_service_order_immutable_fields_are_ignored(self):
        """Garante que customer_id, equipment_id e problem_description não são alterados via PATCH."""
        so = ServiceOrder.objects.create(
            customer=self.customer_1,
            equipment=self.equipment_1,
            problem_description="Descrição original do problema.",
            status=ServiceOrderStatus.RECEBIDO,
        )
        url = reverse("service-order-detail", kwargs={"pk": so.id})
        payload = {
            "customer_id": self.customer_2.id,
            "equipment_id": self.equipment_2.id,
            "problem_description": "Tentativa indevida de alterar a descrição.",
            "status": "aguardando_aprovacao",
        }
        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["customer_id"], self.customer_1.id)
        self.assertEqual(response.data["equipment_id"], self.equipment_1.id)
        self.assertEqual(
            response.data["problem_description"], "Descrição original do problema."
        )
        self.assertEqual(response.data["status"], "aguardando_aprovacao")

        so.refresh_from_db()
        self.assertEqual(so.customer_id, self.customer_1.id)
        self.assertEqual(so.equipment_id, self.equipment_1.id)
        self.assertEqual(so.problem_description, "Descrição original do problema.")
        self.assertEqual(so.status, ServiceOrderStatus.AGUARDANDO_APROVACAO)

    def test_update_service_order_invalid_status_fails(self):
        """Rejeita atualização com status inválido e não altera o banco de dados."""
        so = ServiceOrder.objects.create(
            customer=self.customer_1,
            equipment=self.equipment_1,
            problem_description="Troca de bateria.",
            status=ServiceOrderStatus.RECEBIDO,
        )
        url = reverse("service-order-detail", kwargs={"pk": so.id})
        response = self.client.patch(
            url, {"status": "status_inexistente"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)
        self.assertIn("status", response.data["errors"])

        so.refresh_from_db()
        self.assertEqual(so.status, ServiceOrderStatus.RECEBIDO)

    def test_update_service_order_negative_budget_fails(self):
        """Rejeita orçamento negativo e preserva o estado anterior."""
        so = ServiceOrder.objects.create(
            customer=self.customer_1,
            equipment=self.equipment_1,
            problem_description="Conector solto.",
            status=ServiceOrderStatus.RECEBIDO,
            estimated_budget="100.00",
        )
        url = reverse("service-order-detail", kwargs={"pk": so.id})
        response = self.client.patch(url, {"estimated_budget": "-50.00"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)
        self.assertIn("estimated_budget", response.data["errors"])

        so.refresh_from_db()
        self.assertEqual(str(so.estimated_budget), "100.00")

    def test_update_service_order_nonexistent_order_fails(self):
        """Retorna HTTP 404 quando o identificador da ordem não existe."""
        url = reverse("service-order-detail", kwargs={"pk": 999999})
        response = self.client.patch(url, {"status": "em_diagnostico"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)

    def test_update_service_order_unauthenticated_fails(self):
        """Rejeita atualização sem autenticação com HTTP 401 Unauthorized."""
        so = ServiceOrder.objects.create(
            customer=self.customer_1,
            equipment=self.equipment_1,
            problem_description="Troca de display.",
            status=ServiceOrderStatus.RECEBIDO,
        )
        self.client.credentials()  # Remove token
        url = reverse("service-order-detail", kwargs={"pk": so.id})
        response = self.client.patch(url, {"status": "em_diagnostico"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        so.refresh_from_db()
        self.assertEqual(so.status, ServiceOrderStatus.RECEBIDO)

    def test_update_service_order_nullable_fields_success(self):
        """Permite definir campos opcionais como nulos."""
        so = ServiceOrder.objects.create(
            customer=self.customer_1,
            equipment=self.equipment_1,
            problem_description="Troca de display.",
            status=ServiceOrderStatus.EM_DIAGNOSTICO,
            diagnosis="Display danificado.",
            estimated_budget="200.00",
            notes="Avisar cliente por telefone.",
        )
        url = reverse("service-order-detail", kwargs={"pk": so.id})
        payload = {
            "diagnosis": None,
            "estimated_budget": None,
            "notes": None,
        }
        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data["diagnosis"])
        self.assertIsNone(response.data["estimated_budget"])
        self.assertIsNone(response.data["notes"])

        so.refresh_from_db()
        self.assertIsNone(so.diagnosis)
        self.assertIsNone(so.estimated_budget)
        self.assertIsNone(so.notes)

    def test_openapi_schema_contains_patch_service_orders(self):
        """Valida que o schema OpenAPI documenta a rota PATCH /api/service-orders/{id}/."""
        schema_url = reverse("schema")
        response = self.client.get(schema_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        schema_data = response.data
        self.assertIn("/api/service-orders/{id}/", schema_data["paths"])
        patch_op = schema_data["paths"]["/api/service-orders/{id}/"]["patch"]
        self.assertEqual(patch_op["summary"], "Atualizar ordem de serviço")
        self.assertIn("200", patch_op["responses"])
        self.assertIn("400", patch_op["responses"])
        self.assertIn("401", patch_op["responses"])
        self.assertIn("404", patch_op["responses"])
        self.assertEqual(patch_op["security"], [{"TokenAuth": []}])

    def test_list_service_orders_success(self):
        """Lista todas as ordens de serviço cadastradas ordenadas por -created_at e -id."""
        so1 = ServiceOrder.objects.create(
            customer=self.customer_1,
            equipment=self.equipment_1,
            problem_description="Primeiro atendimento.",
            status=ServiceOrderStatus.RECEBIDO,
        )
        so2 = ServiceOrder.objects.create(
            customer=self.customer_2,
            equipment=self.equipment_2,
            problem_description="Segundo atendimento.",
            status=ServiceOrderStatus.EM_DIAGNOSTICO,
        )

        url = reverse("service-order-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)
        # Ordem padrão: so2 (mais recente), depois so1
        self.assertEqual(response.data[0]["id"], so2.id)
        self.assertEqual(response.data[1]["id"], so1.id)
        self.assertIn("customer_id", response.data[0])
        self.assertIn("equipment_id", response.data[0])
        self.assertIn("problem_description", response.data[0])
        self.assertIn("status", response.data[0])
        self.assertIn("diagnosis", response.data[0])
        self.assertIn("estimated_budget", response.data[0])
        self.assertIn("notes", response.data[0])
        self.assertIn("created_at", response.data[0])
        self.assertIn("updated_at", response.data[0])

    def test_list_service_orders_filter_by_customer_id(self):
        """Filtra a listagem de ordens de serviço por customer_id."""
        so1 = ServiceOrder.objects.create(
            customer=self.customer_1,
            equipment=self.equipment_1,
            problem_description="Ordem cliente 1.",
        )
        ServiceOrder.objects.create(
            customer=self.customer_2,
            equipment=self.equipment_2,
            problem_description="Ordem cliente 2.",
        )

        url = f"{reverse('service-order-list-create')}?customer_id={self.customer_1.id}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], so1.id)
        self.assertEqual(response.data[0]["customer_id"], self.customer_1.id)

    def test_list_service_orders_filter_by_status(self):
        """Filtra a listagem de ordens de serviço por status."""
        so1 = ServiceOrder.objects.create(
            customer=self.customer_1,
            equipment=self.equipment_1,
            problem_description="Ordem em conserto.",
            status=ServiceOrderStatus.EM_CONSERTO,
        )
        ServiceOrder.objects.create(
            customer=self.customer_2,
            equipment=self.equipment_2,
            problem_description="Ordem recebida.",
            status=ServiceOrderStatus.RECEBIDO,
        )

        url = f"{reverse('service-order-list-create')}?status=em_conserto"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], so1.id)
        self.assertEqual(response.data[0]["status"], "em_conserto")

    def test_list_service_orders_filter_by_customer_and_status(self):
        """Combina filtros por customer_id e status."""
        so1 = ServiceOrder.objects.create(
            customer=self.customer_1,
            equipment=self.equipment_1,
            problem_description="Ordem 1 cliente 1 entregue.",
            status=ServiceOrderStatus.ENTREGUE,
        )
        ServiceOrder.objects.create(
            customer=self.customer_1,
            equipment=self.equipment_1,
            problem_description="Ordem 2 cliente 1 recebido.",
            status=ServiceOrderStatus.RECEBIDO,
        )
        ServiceOrder.objects.create(
            customer=self.customer_2,
            equipment=self.equipment_2,
            problem_description="Ordem cliente 2 entregue.",
            status=ServiceOrderStatus.ENTREGUE,
        )

        url = f"{reverse('service-order-list-create')}?customer_id={self.customer_1.id}&status=entregue"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], so1.id)
        self.assertEqual(response.data[0]["customer_id"], self.customer_1.id)
        self.assertEqual(response.data[0]["status"], "entregue")

    def test_list_service_orders_includes_closed_orders_without_filter(self):
        """Garante que a listagem sem filtros inclui ordens com status entregue e cancelado."""
        so1 = ServiceOrder.objects.create(
            customer=self.customer_1,
            equipment=self.equipment_1,
            problem_description="Ordem ativa.",
            status=ServiceOrderStatus.EM_CONSERTO,
        )
        so2 = ServiceOrder.objects.create(
            customer=self.customer_1,
            equipment=self.equipment_1,
            problem_description="Ordem entregue.",
            status=ServiceOrderStatus.ENTREGUE,
        )
        so3 = ServiceOrder.objects.create(
            customer=self.customer_2,
            equipment=self.equipment_2,
            problem_description="Ordem cancelada.",
            status=ServiceOrderStatus.CANCELADO,
        )

        url = reverse("service-order-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        retrieved_ids = [item["id"] for item in response.data]
        self.assertIn(so1.id, retrieved_ids)
        self.assertIn(so2.id, retrieved_ids)
        self.assertIn(so3.id, retrieved_ids)

    def test_list_service_orders_invalid_customer_id_filter_fails(self):
        """Rejeita filtro customer_id não numérico com HTTP 400."""
        url = f"{reverse('service-order-list-create')}?customer_id=abc"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)
        self.assertIn("customer_id", response.data["errors"])

    def test_list_service_orders_invalid_status_filter_fails(self):
        """Rejeita filtro status inválido com HTTP 400."""
        url = f"{reverse('service-order-list-create')}?status=status_invalido"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)
        self.assertIn("status", response.data["errors"])

    def test_list_service_orders_unauthenticated_fails(self):
        """Rejeita listagem sem token com HTTP 401 Unauthorized."""
        self.client.credentials()
        url = reverse("service-order-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_service_order_detail_success(self):
        """Consulta os dados completos de uma ordem existente."""
        so = ServiceOrder.objects.create(
            customer=self.customer_1,
            equipment=self.equipment_1,
            problem_description="Troca de bateria.",
            status=ServiceOrderStatus.EM_DIAGNOSTICO,
            diagnosis="Bateria inchada.",
            estimated_budget="150.00",
            notes="Avisar cliente via WhatsApp.",
        )
        url = reverse("service-order-detail", kwargs={"pk": so.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], so.id)
        self.assertEqual(response.data["customer_id"], self.customer_1.id)
        self.assertEqual(response.data["equipment_id"], self.equipment_1.id)
        self.assertEqual(response.data["problem_description"], "Troca de bateria.")
        self.assertEqual(response.data["status"], "em_diagnostico")
        self.assertEqual(response.data["diagnosis"], "Bateria inchada.")
        self.assertEqual(response.data["estimated_budget"], "150.00")
        self.assertEqual(response.data["notes"], "Avisar cliente via WhatsApp.")
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)

    def test_retrieve_service_order_detail_nonexistent_fails(self):
        """Retorna HTTP 404 quando o identificador da ordem não existe."""
        url = reverse("service-order-detail", kwargs={"pk": 999999})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)

    def test_retrieve_service_order_detail_unauthenticated_fails(self):
        """Rejeita consulta sem token com HTTP 401 Unauthorized."""
        so = ServiceOrder.objects.create(
            customer=self.customer_1,
            equipment=self.equipment_1,
            problem_description="Sem imagem.",
        )
        self.client.credentials()
        url = reverse("service-order-detail", kwargs={"pk": so.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_close_service_order_as_entregue_success(self):
        """Encerra a ordem marcando status como entregue via PATCH e mantém consultável."""
        so = ServiceOrder.objects.create(
            customer=self.customer_1,
            equipment=self.equipment_1,
            problem_description="Troca de tela.",
            status=ServiceOrderStatus.PRONTO,
            diagnosis="Tela trocada com sucesso.",
            estimated_budget="400.00",
            notes="Garantia de 90 dias.",
        )
        url = reverse("service-order-detail", kwargs={"pk": so.id})
        response = self.client.patch(url, {"status": "entregue"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "entregue")
        self.assertEqual(response.data["diagnosis"], "Tela trocada com sucesso.")
        self.assertEqual(response.data["estimated_budget"], "400.00")
        self.assertEqual(response.data["notes"], "Garantia de 90 dias.")

        # Valida que permanece consultável por GET detail
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data["status"], "entregue")

        # Valida que permanece visível na listagem
        list_url = reverse("service-order-list-create")
        list_response = self.client.get(list_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(item["id"] == so.id for item in list_response.data))

    def test_close_service_order_as_cancelado_success(self):
        """Encerra a ordem marcando status como cancelado via PATCH e mantém consultável."""
        so = ServiceOrder.objects.create(
            customer=self.customer_1,
            equipment=self.equipment_1,
            problem_description="Troca de placa-mãe.",
            status=ServiceOrderStatus.AGUARDANDO_APROVACAO,
            diagnosis="Orçamento não aprovado pelo cliente.",
            estimated_budget="900.00",
        )
        url = reverse("service-order-detail", kwargs={"pk": so.id})
        payload = {
            "status": "cancelado",
            "notes": "Cliente optou por não realizar o serviço.",
        }
        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "cancelado")
        self.assertEqual(
            response.data["notes"], "Cliente optou por não realizar o serviço."
        )

        # Valida persistência
        so.refresh_from_db()
        self.assertEqual(so.status, ServiceOrderStatus.CANCELADO)
        self.assertEqual(so.notes, "Cliente optou por não realizar o serviço.")

        # Valida permanência na consulta
        get_response = self.client.get(url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data["status"], "cancelado")

    def test_openapi_schema_contains_list_and_detail_service_orders(self):
        """Valida que o OpenAPI documenta GET list com parâmetros e GET detail."""
        schema_url = reverse("schema")
        response = self.client.get(schema_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        schema_data = response.data

        # GET /api/service-orders/
        self.assertIn("/api/service-orders/", schema_data["paths"])
        get_list_op = schema_data["paths"]["/api/service-orders/"]["get"]
        self.assertEqual(get_list_op["summary"], "Listar ordens de serviço")
        self.assertIn("200", get_list_op["responses"])
        self.assertIn("400", get_list_op["responses"])
        self.assertIn("401", get_list_op["responses"])
        param_names = [p["name"] for p in get_list_op.get("parameters", [])]
        self.assertIn("customer_id", param_names)
        self.assertIn("status", param_names)

        # GET /api/service-orders/{id}/
        self.assertIn("/api/service-orders/{id}/", schema_data["paths"])
        get_detail_op = schema_data["paths"]["/api/service-orders/{id}/"]["get"]
        self.assertEqual(get_detail_op["summary"], "Consultar ordem de serviço")
        self.assertIn("200", get_detail_op["responses"])
        self.assertIn("401", get_detail_op["responses"])
        self.assertIn("404", get_detail_op["responses"])
