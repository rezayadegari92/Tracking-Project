from django import forms
from .models import Shipper, Shipment

class ShipperForm(forms.ModelForm):
    class Meta:
        model = Shipper
        fields = '__all__'

class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = [
            'receiver_name', 'receiver_address', 'receiver_country', 'receiver_city',
            'receiver_location', 'receiver_contact_person', 'receiver_contact_number', 'receiver_mobile_number',
            'awb_number', 'reference_number', 'booking_date', 'booking_time', 'product_type', 'pieces',
            'weight', 'v_weight', 'c_weight', 'item_description', 'special_instruction',
            'cod_amount', 'base_price', 'additional_charges'
        ]

