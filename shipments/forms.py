from django import forms
from .models import Shipper, Shipment
from cities_light.models import Country, City

class ShipperForm(forms.ModelForm):
    shipper_country = forms.ModelChoiceField(
        queryset=Country.objects.all().order_by('name'),
        widget=forms.Select(attrs={'class': 'form-control country-select'})
    )
    shipper_city = forms.ModelChoiceField(
        queryset=City.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control city-select'})
    )

    class Meta:
        model = Shipper
        exclude = ['created_at', 'updated_at', 'country', 'city']
        widgets = {
            'shipper_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter shipper name'}),
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Enter complete address'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location details'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact person name'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact number'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}),
            'identity_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'shipper_country' in self.data:
            try:
                country_id = int(self.data.get('shipper_country'))
                self.fields['shipper_city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.country:
            self.fields['shipper_city'].queryset = self.instance.country.city_set.order_by('name')

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.country = self.cleaned_data['shipper_country']
        instance.city = self.cleaned_data['shipper_city']
        if commit:
            instance.save()
        return instance

class ShipmentForm(forms.ModelForm):
    receiver_country = forms.ModelChoiceField(
        queryset=Country.objects.all().order_by('name'),
        widget=forms.Select(attrs={'class': 'form-control country-select'})
    )
    receiver_city = forms.ModelChoiceField(
        queryset=City.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control city-select'})
    )
    identity_image = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        })
    )

    class Meta:
        model = Shipment
        exclude = ['created_at', 'updated_at', 'awb_number', 'reference_number', 'shipper', 'receiver_country', 'receiver_city']
        widgets = {
            'receiver_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter receiver name'}),
            'receiver_address': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Enter complete address'}),
            'receiver_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location details'}),
            'receiver_contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact person name'}),
            'receiver_contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact number'}),
            'receiver_mobile_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}),
            'item_description': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Enter item description'}),
            'special_instruction': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Enter special instructions if any'}),
            'grossweight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter weight in kg'}),
            'width': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter width in cm'}),
            'length': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter length in cm'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter height in cm'}),
            'price_of_shipment': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter price'}),
            'cod_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter COD amount'}),
            'base_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter base price'}),
            'additional_charges': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter additional charges'}),
            'product_type': forms.Select(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'receiver_country' in self.data:
            try:
                country_id = int(self.data.get('receiver_country'))
                self.fields['receiver_city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.receiver_country:
            self.fields['receiver_city'].queryset = self.instance.receiver_country.city_set.order_by('name')

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.receiver_country = self.cleaned_data['receiver_country']
        instance.receiver_city = self.cleaned_data['receiver_city']
        if commit:
            instance.save()
        return instance

