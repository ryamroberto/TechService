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
        indexes = (
            models.Index(fields=["status"], name="so_status_idx"),
            models.Index(fields=["customer", "status"], name="so_customer_status_idx"),
            models.Index(fields=["-created_at"], name="so_created_at_desc_idx"),
        )
        constraints = (
            models.CheckConstraint(
                condition=models.Q(estimated_budget__gte=Decimal("0.00"))
                | models.Q(estimated_budget__isnull=True),
                name="service_order_estimated_budget_non_negative",
            ),
            models.CheckConstraint(
                condition=models.Q(status__in=ServiceOrderStatus.values),
                name="service_order_status_valid",
            ),
        )

    def __str__(self):
        return f"OS #{self.id} - {self.customer.name} ({self.get_status_display()})"
