from django import forms
from .models import Shipment, Sender, Receiver, ShipmentCost

class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = '__all__'

class SenderForm(forms.ModelForm):
    class Meta:
        model = Sender
        fields = '__all__'

class ReceiverForm(forms.ModelForm):
    class Meta:
        model = Receiver
        fields = '__all__'

class ShipmentCostForm(forms.ModelForm):
    class Meta:
        model = ShipmentCost
        fields = '__all__'