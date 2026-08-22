from django.apps import AppConfig


class CustomersConfig(AppConfig):
    """Configuração do app de clientes."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.customers"
