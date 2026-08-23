from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from apps.customers.models import Customer


class CustomerApiTests(APITestCase):
    """Testes dos endpoints protegidos de clientes."""

    def setUp(self):
        user = get_user_model().objects.create_user(
            username="atendente",
            password="senha-segura-123",
        )
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        self.list_url = reverse("customers:customer-list-create")

    def customer_payload(self, **overrides):
        payload = {
            "name": "Maria da Silva",
            "phone": "(11) 99999-9999",
            "email": "maria@example.com",
        }
        payload.update(overrides)
        return payload

    def test_create_customer_with_required_data(self):
        response = self.client.post(
            self.list_url,
            self.customer_payload(),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(response.data["name"], "Maria da Silva")
        self.assertEqual(response.data["email"], "maria@example.com")
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)

    def test_create_customer_requires_name_and_phone(self):
        response = self.client.post(
            self.list_url,
            {"email": "maria@example.com"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data)
        self.assertIn("name", response.data["errors"])
        self.assertIn("phone", response.data["errors"])
        self.assertEqual(Customer.objects.count(), 0)

    def test_create_customer_rejects_invalid_email(self):
        response = self.client.post(
            self.list_url,
            self.customer_payload(email="email-invalido"),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data["errors"])
        self.assertEqual(Customer.objects.count(), 0)

    def test_list_customers(self):
        Customer.objects.create(**self.customer_payload())
        Customer.objects.create(
            **self.customer_payload(
                name="João Souza",
                phone="(11) 98888-8888",
                email=None,
            )
        )

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["name"], "Maria da Silva")
        self.assertEqual(response.data[1]["name"], "João Souza")

    def test_retrieve_customer(self):
        customer = Customer.objects.create(**self.customer_payload())

        response = self.client.get(
            reverse("customers:customer-detail", args=[customer.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], customer.pk)
        self.assertEqual(response.data["phone"], customer.phone)

    def test_retrieve_missing_customer_returns_404(self):
        response = self.client.get(reverse("customers:customer-detail", args=[99999]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"detail": "Not found."})

    def test_patch_customer_partially(self):
        customer = Customer.objects.create(**self.customer_payload())

        response = self.client.patch(
            reverse("customers:customer-detail", args=[customer.pk]),
            {"phone": "(11) 97777-7777"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        customer.refresh_from_db()
        self.assertEqual(customer.phone, "(11) 97777-7777")
        self.assertEqual(customer.name, "Maria da Silva")

    def test_patch_customer_rejects_invalid_email(self):
        customer = Customer.objects.create(**self.customer_payload())

        response = self.client.patch(
            reverse("customers:customer-detail", args=[customer.pk]),
            {"email": "email-invalido"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data["errors"])

    def test_customer_operations_require_token(self):
        customer = Customer.objects.create(**self.customer_payload())
        detail_url = reverse("customers:customer-detail", args=[customer.pk])
        self.client.credentials()

        list_response = self.client.get(self.list_url)
        create_response = self.client.post(
            self.list_url,
            self.customer_payload(),
            format="json",
        )
        detail_response = self.client.get(detail_url)
        patch_response = self.client.patch(
            detail_url,
            {"phone": "(11) 96666-6666"},
            format="json",
        )

        for response in (
            list_response,
            create_response,
            detail_response,
            patch_response,
        ):
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_openapi_documents_customer_contract(self):
        response = self.client.get(reverse("schema"))
        schema_text = response.content.decode()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("/api/customers/:", schema_text)
        self.assertIn("CustomerInput:", schema_text)
        self.assertIn("Customer:", schema_text)
        self.assertIn("TokenAuth:", schema_text)
