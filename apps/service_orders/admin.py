from django.contrib import admin

from apps.service_orders.models import ServiceOrder


@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "equipment",
        "status",
        "estimated_budget",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "customer__name",
        "equipment__brand",
        "equipment__model",
        "problem_description",
        "diagnosis",
    )
    list_filter = ("status", "created_at")
