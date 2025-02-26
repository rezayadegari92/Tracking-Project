from django.urls import path
from .views import create_shipment, shipment_detail



urlpatterns = [

    path('create/', create_shipment, name='create_shipment'),

    path('shipment/<int:shipment_id>', shipment_detail, name='shipment_detail'),

]

