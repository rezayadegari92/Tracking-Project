from django.urls import path
from .views import (
    CountryListView, CityListView, ShipmentCreateView, ShipmentListView,
    ShipmentDetailView, track_shipment, ShipmentConfirmationPDFView,
    ShipmentDetailedPDFView, ShipmentLabelPDFView
)

urlpatterns = [
    # Public endpoints
    path('countries/', CountryListView.as_view(), name='country-list'),
    path('cities/', CityListView.as_view(), name='city-list'),
    path('', ShipmentCreateView.as_view(), name='shipment-create'),
    path('track/', track_shipment, name='shipment-track'),
    
    # Authenticated endpoints
    path('list/', ShipmentListView.as_view(), name='shipment-list'),
    path('<int:id>/', ShipmentDetailView.as_view(), name='shipment-detail'),
    
    # PDF endpoints
    path('<int:id>/pdf/confirmation/', ShipmentConfirmationPDFView.as_view(), name='shipment-confirmation-pdf'),
    path('<int:id>/pdf/detailed/', ShipmentDetailedPDFView.as_view(), name='shipment-detailed-pdf'),
    path('<int:id>/pdf/label/', ShipmentLabelPDFView.as_view(), name='shipment-label-pdf'),
]
