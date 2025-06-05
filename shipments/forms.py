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
    """Form for creating and updating shipments."""
    class Meta:
        model = Shipment
        exclude = ['shipper', 'awb_number', 'reference_number', 'payment_status', 'chargeable_weight', 'volumetricks']
        widgets = {
            'receiver_country': forms.Select(attrs={'class': 'form-control'}),
            'receiver_city': forms.Select(attrs={'class': 'form-control'}),
            'product_type': forms.Select(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'booking_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'booking_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'item_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'special_instruction': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'length': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'width': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'grossweight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make certain fields optional for user creation
        self.fields['price_of_shipment'].required = False
        self.fields['base_price'].required = False
        self.fields['cod_amount'].required = False
        self.fields['additional_charges'].required = False
        
        # Add custom error messages
        self.fields['receiver_name'].error_messages = {
            'required': 'Receiver name is required.',
            'max_length': 'Receiver name cannot exceed 100 characters.'
        }
        self.fields['receiver_address'].error_messages = {
            'required': 'Receiver address is required.'
        }
        self.fields['receiver_contact_person'].error_messages = {
            'required': 'Receiver contact person is required.',
            'max_length': 'Contact person name cannot exceed 100 characters.'
        }
        self.fields['receiver_contact_number'].error_messages = {
            'required': 'Receiver contact number is required.',
            'max_length': 'Contact number cannot exceed 20 characters.'
        }
        self.fields['quantity'].error_messages = {
            'required': 'Quantity is required.',
            'min_value': 'Quantity must be greater than 0.'
        }
        self.fields['grossweight'].error_messages = {
            'required': 'Weight is required.',
            'min_value': 'Weight must be greater than 0.'
        }
        self.fields['length'].error_messages = {
            'required': 'Length is required.',
            'min_value': 'Length must be greater than 0.'
        }
        self.fields['width'].error_messages = {
            'required': 'Width is required.',
            'min_value': 'Width must be greater than 0.'
        }
        self.fields['height'].error_messages = {
            'required': 'Height is required.',
            'min_value': 'Height must be greater than 0.'
        }
        self.fields['item_description'].error_messages = {
            'required': 'Item description is required.'
        }

    def clean(self):
        cleaned_data = super().clean()
        # Validate dimensions and weight
        length = cleaned_data.get('length')
        width = cleaned_data.get('width')
        height = cleaned_data.get('height')
        quantity = cleaned_data.get('quantity')
        grossweight = cleaned_data.get('grossweight')

        if all([length, width, height, quantity, grossweight]):
            # Calculate volumetric weight
            volumetric_weight = (length * width * height * quantity) / 5000
            # Calculate chargeable weight
            chargeable_weight = max(volumetric_weight, grossweight)
            
            # Store calculated values in cleaned_data
            cleaned_data['volumetricks'] = volumetric_weight
            cleaned_data['chargeable_weight'] = chargeable_weight

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Ensure payment status is set to pending for new shipments
        instance.payment_status = 'pending'
        if commit:
            try:
                instance.save()
            except Exception as e:
                raise forms.ValidationError(f"Error saving shipment: {str(e)}")
        return instance

