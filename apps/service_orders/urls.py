from django.urls import path

from apps.service_orders.views import ServiceOrderCreateView

urlpatterns = [
    path("", ServiceOrderCreateView.as_view(), name="service-order-create"),
]
