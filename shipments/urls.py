from django.urls import path
from .views import *



urlpatterns = [
    path('', home, name = 'home'),
    path('save/', save_shipper_and_shipment, name='save_shipper_and_shipment'),
    # path('create/', create_shipment, name='create_shipment'),
    #
    # path('shipment/<int:shipment_id>', shipment_detail, name='shipment_detail'),

]

