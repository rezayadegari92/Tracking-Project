from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import *

def home(request):
    reference_number = request.GET.get('reference_number')
    shipment = None

    if reference_number:
        try:
            shipment = Shipment.objects.get(reference_number=reference_number)
        except Shipment.DoesNotExist:
            # If no shipment is found, display a user-friendly error message
            messages.error(request, f'No shipment found with the reference number: {reference_number}')
    elif 'reference_number' in request.GET:  # Check if reference_number is provided but empty
        messages.error(request, 'Reference number is invalid. Please enter a valid reference number.')

    return render(request, 'home.html', {'shipment': shipment})




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

