from django.urls import path
from .views import create_shipment, shipment_list



urlpatterns = [

    path('create/', create_shipment, name='create_shipment'),

    path('list/', shipment_list, name='shipment_list'),

]

