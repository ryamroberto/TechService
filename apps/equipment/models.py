from django.db import models


class Equipment(models.Model):
    """Representa um equipamento de cliente registrado para atendimento."""

    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.CASCADE,
        related_name="equipment",
    )
    type = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    identifier = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "equipment"
        ordering = ("id",)

    def __str__(self):
        return f"{self.type} {self.brand} {self.model} (#{self.id})"
