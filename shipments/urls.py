from django.urls import path
from .views import (
    home, create_shipment, shipment_detail, load_cities,
    ShipmentTrackingView
)

urlpatterns = [
    path('', home, name='home'),
    path('create/', create_shipment, name='create_shipment'),
    path('shipment/<int:pk>/', shipment_detail, name='shipment_detail'),
    path('track/', ShipmentTrackingView.as_view(), name='track_shipment'),
    path('ajax/load-cities/', load_cities, name='load_cities'),
]

