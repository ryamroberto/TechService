from django.urls import path

from apps.equipment.views import EquipmentDetailView, EquipmentListCreateView

urlpatterns = [
    path("", EquipmentListCreateView.as_view(), name="equipment-list-create"),
    path("<int:pk>/", EquipmentDetailView.as_view(), name="equipment-detail"),
]
