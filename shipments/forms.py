from django import forms

from .models import Shipment



class ShipmentForm(forms.ModelForm):

    class Meta:

        model = Shipment

        fields = '__all__'

        widgets = {

            'shipper_address': forms.Textarea(attrs={'rows': 2}),

            'receiver_address': forms.Textarea(attrs={'rows': 2}),

            'special_instruction': forms.Textarea(attrs={'rows': 2}),

            'item_description': forms.Textarea(attrs={'rows': 2}),

            'booking_date': forms.DateInput(attrs={'type': 'date'}),

            'booking_time': forms.TimeInput(attrs={'type': 'time'}),
        }