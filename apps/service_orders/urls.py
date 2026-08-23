from django.urls import path

from apps.service_orders.views import (
    ServiceOrderCreateView,
    ServiceOrderDetailView,
)

urlpatterns = [
    path("", ServiceOrderCreateView.as_view(), name="service-order-create"),
    path("<int:pk>/", ServiceOrderDetailView.as_view(), name="service-order-detail"),
]
