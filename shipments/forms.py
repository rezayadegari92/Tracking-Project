from django import forms

from .models import Shipment, Address, Country, City, Shipper



class ShipmentForm(forms.ModelForm):

    class Meta:

        model = Shipment

        fields = '__all__'

        widgets = {

            'booking_date': forms.DateInput(attrs={'type': 'date'}),

            'booking_time': forms.TimeInput(attrs={'type': 'time'}),

            'special_instruction': forms.Textarea(attrs={'rows': 2}),

            'item_description': forms.Textarea(attrs={'rows': 2}),

        }



    def __init__(self, *args, **kwargs):

        user = kwargs.pop('user', None)  # گرفتن یوزر لاگین شده

        super().__init__(*args, **kwargs)



        # اگر کاربر لاگین کرده باشه، اطلاعات فرستنده رو به‌طور خودکار پر کن

        if user and hasattr(user, 'shipper'):

            self.fields['shipper'].initial = user.shipper



        # برای فیلد کشور و شهر، مقادیر موجود رو در لیست انتخابی نمایش بده

        self.fields['receiver_address'].queryset = Address.objects.all()

