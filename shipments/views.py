

def home(request):
    reference_number = request.GET.get('reference_number')
    shipment = None
    if reference_number:
        shipment = get_object_or_404(Shipment, reference_number=reference_number)
    return render(request, 'home.html', {'shipment': shipment})

from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Shipper, Shipment
from .forms import ShipperForm, ShipmentForm

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Shipper, Shipment

def save_shipper_and_shipment(request):
    if request.method == 'POST':
        try:
            # Save Shipper
            shipper = Shipper(
                shipper_name=request.POST['shipper_name'],
                address=request.POST['address'],
                country=request.POST['country'],
                city=request.POST['city'],
                location=request.POST.get('location', ''),
                contact_person=request.POST['contact_person'],
                contact_number=request.POST['contact_number'],
                mobile_number=request.POST.get('mobile_number', '')
            )
            shipper.save()

            # Save Shipment
            shipment = Shipment(
                shipper=shipper,
                receiver_name=request.POST['receiver_name'],
                receiver_address=request.POST['receiver_address'],
                receiver_country=request.POST['receiver_country'],
                receiver_city=request.POST['receiver_city'],
                receiver_location=request.POST.get('receiver_location', ''),
                receiver_contact_person=request.POST['receiver_contact_person'],
                receiver_contact_number=request.POST['receiver_contact_number'],
                receiver_mobile_number=request.POST.get('receiver_mobile_number', ''),
                awb_number=request.POST['awb_number'],
                reference_number=request.POST.get('reference_number', ''),
                booking_date=request.POST['booking_date'],
                booking_time=request.POST['booking_time'],
                product_type=request.POST['product_type'],
                pieces=request.POST['pieces'],
                weight=request.POST['weight'],
                v_weight=request.POST['v_weight'],
                c_weight=request.POST['c_weight'],
                item_description=request.POST['item_description'],
                special_instruction=request.POST.get('special_instruction', ''),
                cod_amount=request.POST['cod_amount'],
                base_price=request.POST['base_price'],
                additional_charges=request.POST['additional_charges']
            )
            shipment.save()

            # Add a success message
            messages.success(request, 'Shipper and Shipment saved successfully!')
        except Exception as e:
            # Add an error message if something goes wrong
            messages.error(request, f'An error occurred: {str(e)}')

    return render(request, 'shipment_form.html')

