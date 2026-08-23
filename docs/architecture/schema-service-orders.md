# Especificação de Schema: `service_orders` (Épico 3)

> **Autor:** @data-engineer (Dara — Master Database Architect & Reliability Engineer)  
> **Data:** 22/08/2026  
> **Status:** Aprovado / Pronto para Implementação (@dev)  
> **Stories Relacionadas:** Story 3.1, Story 3.2, Story 3.3  

---

## 1. Visão Geral do Schema

A tabela `service_orders` gerencia o ciclo de vida dos atendimentos técnicos, vinculando clientes e seus respectivos equipamentos aos registros de diagnóstico, orçamento e execução de serviços.

### Definição DDL (PostgreSQL / SQLite)

```sql
CREATE TABLE service_orders (
    id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL REFERENCES customers(id) ON DELETE RESTRICT,
    equipment_id BIGINT NOT NULL REFERENCES equipment(id) ON DELETE RESTRICT,
    problem_description TEXT NOT NULL,
    status VARCHAR(25) NOT NULL DEFAULT 'recebido',
    diagnosis TEXT NULL,
    estimated_budget NUMERIC(10, 2) NULL,
    notes TEXT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT service_order_estimated_budget_non_negative 
        CHECK (estimated_budget >= 0.00 OR estimated_budget IS NULL),
    CONSTRAINT service_order_status_valid 
        CHECK (status IN ('recebido', 'em_diagnostico', 'aguardando_aprovacao', 'em_conserto', 'pronto', 'entregue', 'cancelado'))
);

-- Índices
CREATE INDEX service_orders_customer_id_idx ON service_orders (customer_id);
CREATE INDEX service_orders_equipment_id_idx ON service_orders (equipment_id);
CREATE INDEX so_status_idx ON service_orders (status);
CREATE INDEX so_customer_status_idx ON service_orders (customer_id, status);
CREATE INDEX so_created_at_desc_idx ON service_orders (created_at DESC);
```

---

## 2. Decisões de Arquitetura de Dados

### 2.1 Estratégia de Deleção (`on_delete`)
- **`customer`:** `models.PROTECT`
- **`equipment`:** `models.PROTECT`
- **Racional:** Ordens de serviço são registros com valor histórico, legal e operacional. Qualquer exclusão em cascata (`CASCADE`) causaria perda destrutiva de dados. A tentativa de remover um cliente ou equipamento com ordens registradas é bloqueada via `django.db.models.ProtectedError`.

### 2.2 Constraints de Integridade
1. **`service_order_estimated_budget_non_negative`:** Impede que orçamentos com valor negativo sejam persistidos no banco (`CHECK (estimated_budget >= 0.00 OR estimated_budget IS NULL)`).
2. **`service_order_status_valid`:** Impede que valores arbitrários de status sejam inseridos via SQL manual ou migrações imperfeitas (`CHECK (status IN (...))`).

### 2.3 Estratégia de Índices
1. **`customer_id` & `equipment_id`:** Criados automaticamente pelo ORM do Django.
2. **`so_status_idx`:** Otimiza consultas filtrando por fila/status (`recebido`, `em_conserto`, etc.).
3. **`so_customer_status_idx`:** Otimiza a busca composta de atendimentos por cliente filtrando por status (Story 3.3).
4. **`so_created_at_desc_idx`:** Otimiza ordenação padrão decrescente (`-created_at`, `-id`).

---

## 3. Blueprint do Modelo Django (`apps/service_orders/models.py`)

```python
from decimal import Decimal
from django.db import models


class ServiceOrderStatus(models.TextChoices):
    RECEBIDO = "recebido", "Recebido"
    EM_DIAGNOSTICO = "em_diagnostico", "Em diagnóstico"
    AGUARDANDO_APROVACAO = "aguardando_aprovacao", "Aguardando aprovação"
    EM_CONSERTO = "em_conserto", "Em conserto"
    PRONTO = "pronto", "Pronto"
    ENTREGUE = "entregue", "Entregue"
    CANCELADO = "cancelado", "Cancelado"


class ServiceOrder(models.Model):
    """Representa uma ordem de serviço de manutenção de equipamento."""

    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.PROTECT,
        related_name="service_orders",
    )
    equipment = models.ForeignKey(
        "equipment.Equipment",
        on_delete=models.PROTECT,
        related_name="service_orders",
    )
    problem_description = models.TextField()
    status = models.CharField(
        max_length=25,
        choices=ServiceOrderStatus.choices,
        default=ServiceOrderStatus.RECEBIDO,
    )
    diagnosis = models.TextField(blank=True, null=True)
    estimated_budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "service_orders"
        ordering = ("-created_at", "-id")
        indexes = [
            models.Index(fields=["status"], name="so_status_idx"),
            models.Index(fields=["customer", "status"], name="so_customer_status_idx"),
            models.Index(fields=["-created_at"], name="so_created_at_desc_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(estimated_budget__gte=Decimal("0.00"))
                | models.Q(estimated_budget__isnull=True),
                name="service_order_estimated_budget_non_negative",
            ),
            models.CheckConstraint(
                condition=models.Q(status__in=ServiceOrderStatus.values),
                name="service_order_status_valid",
            ),
        ]

    def __str__(self):
        return f"OS #{self.id} - {self.customer.name} ({self.get_status_display()})"
```

---

## 4. Plano de Migração

- **Pacote:** `apps/service_orders/migrations/0001_initial.py`
- **Dependências Declaradas:**
  ```python
  dependencies = [
      ("customers", "0001_initial"),
      ("equipment", "0001_initial"),
  ]
  ```
- **Execução:**
  ```bash
  python manage.py makemigrations service_orders
  python manage.py migrate
  ```
- **Rollback seguro:**
  ```bash
  python manage.py migrate service_orders zero
  ```

---

— Dara, arquitetando dados 🗄️
