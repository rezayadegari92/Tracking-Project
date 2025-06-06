from django.urls import path
from .views import (
    home, create_shipment, shipment_detail, load_cities,
    ShipmentTrackingView, shipment_confirmation_pdf, shipment_detailed_pdf,
    shipment_label_pdf, shipment_pdf, shipment_label_by_awb
)

urlpatterns = [
    path('', home, name='home'),
    path('create/', create_shipment, name='create_shipment'),
    path('shipment/<int:pk>/', shipment_detail, name='shipment_detail'),
    path('track/', ShipmentTrackingView.as_view(), name='track_shipment'),
    path('ajax/load-cities/', load_cities, name='load_cities'),
    path('shipment/<int:shipment_id>/confirmation-pdf/', shipment_confirmation_pdf, name='shipment_confirmation_pdf'),
    path('shipment/<int:shipment_id>/detailed-pdf/', shipment_detailed_pdf, name='shipment_detailed_pdf'),
    path('shipment/<int:shipment_id>/label/', shipment_label_pdf, name='shipment_label_pdf'),
    path('shipment/<str:awb_number>/pdf/', shipment_pdf, name='shipment_pdf'),
    path('shipment/<str:awb_number>/label/', shipment_label_by_awb, name='shipment_label_by_awb'),
]

