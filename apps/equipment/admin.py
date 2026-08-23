from django.contrib import admin

from apps.equipment.models import Equipment


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "type",
        "brand",
        "model",
        "identifier",
        "created_at",
    )
    search_fields = ("brand", "model", "identifier", "customer__name")
    list_filter = ("type", "brand")
