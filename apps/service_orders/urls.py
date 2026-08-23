from django.urls import path

from apps.service_orders.views import (
    ServiceOrderDetailView,
    ServiceOrderListCreateView,
)

urlpatterns = [
    path("", ServiceOrderListCreateView.as_view(), name="service-order-list-create"),
    path("", ServiceOrderListCreateView.as_view(), name="service-order-create"),
    path("<int:pk>/", ServiceOrderDetailView.as_view(), name="service-order-detail"),
]
