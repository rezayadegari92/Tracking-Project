from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import *
from django.views.generic import TemplateView, View
from django.http import JsonResponse, HttpResponse
from cities_light.models import Country, City
from .forms import ShipperForm, ShipmentForm
from django.contrib.admin.views.decorators import staff_member_required
from .utils.pdf_generator import (
    generate_shipment_confirmation_pdf,
    generate_shipment_detailed_pdf,
    generate_shipment_label_pdf
)
from django.utils import timezone
from django.db import transaction

def home(request):
    tracking_number = request.GET.get('tracking_number', '')
    shipment = None
    error = None

    if tracking_number:
        if tracking_number.startswith('AWB-'):
            shipment = Shipment.objects.filter(awb_number=tracking_number).first()
        elif tracking_number.startswith('REF-'):
            shipment = Shipment.objects.filter(reference_number=tracking_number).first()
        else:
            error = "Invalid tracking number format. Please use AWB- or REF- prefix."
        
        if not shipment and not error:
            error = "No shipment found with this tracking number."

    return render(request, 'shipments/home.html', {
        'shipment': shipment,
        'tracking_number': tracking_number,
        'error': error
    })



from django.contrib.auth.decorators import login_required

# @login_required()
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


class ShipmentTrackingView(View):
    def get(self, request, *args, **kwargs):
        tracking_number = request.GET.get('tracking_number')
        if not tracking_number:
            return JsonResponse({'error': 'Tracking number is required'}, status=400)
        
        try:
            if tracking_number.startswith('AWB-'):
                shipment = Shipment.objects.get(awb_number=tracking_number)
            elif tracking_number.startswith('REF-'):
                shipment = Shipment.objects.get(reference_number=tracking_number)
            else:
                return JsonResponse({'error': 'Invalid tracking number format'}, status=400)
            
            data = {
                'status': shipment.status,
                'current_location': shipment.current_location,
                'estimated_delivery': shipment.estimated_delivery,
                'shipper_name': shipment.shipper.shipper_name,
                'receiver_name': shipment.receiver_name,
            }
            return JsonResponse(data)
        except Shipment.DoesNotExist:
            return JsonResponse({'error': 'Shipment not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def create_shipment(request):
    if request.method == 'POST':
        print("POST request received")
        shipper_form = ShipperForm(request.POST)
        shipment_form = ShipmentForm(request.POST, request.FILES)
        
        print("Shipper form errors:", shipper_form.errors if not shipper_form.is_valid() else "No errors")
        print("Shipment form errors:", shipment_form.errors if not shipment_form.is_valid() else "No errors")
        
        if shipper_form.is_valid() and shipment_form.is_valid():
            try:
                with transaction.atomic():
                    shipper = shipper_form.save()
                    shipment = shipment_form.save(commit=False)
                    shipment.shipper = shipper
                    shipment.payment_status = 'pending'  # Set initial payment status
                    shipment.save()
                    
                    # Save the identity image
                    if 'identity_image' in request.FILES:
                        ShipmentImage.objects.create(
                            shipment=shipment,
                            image=request.FILES['identity_image']
                        )
                    
                messages.success(request, 'Shipment created successfully!')
                return redirect('shipment_detail', pk=shipment.pk)
            except Exception as e:
                print(f"Error saving shipment: {str(e)}")
                messages.error(request, f'Error creating shipment: {str(e)}')
                # Add form-level error
                shipment_form.add_error(None, str(e))
        else:
            # Display form-specific errors
            for field, errors in shipper_form.errors.items():
                for error in errors:
                    messages.error(request, f'Shipper {field}: {error}')
            for field, errors in shipment_form.errors.items():
                for error in errors:
                    messages.error(request, f'Shipment {field}: {error}')
    else:
        shipper_form = ShipperForm()
        shipment_form = ShipmentForm()
    
    return render(request, 'shipments/shipment_form.html', {
        'form': shipment_form,
        'shipper_form': shipper_form,
        'messages': messages.get_messages(request)
    })

def shipment_detail(request, pk):
    shipment = get_object_or_404(Shipment, pk=pk)
    return render(request, 'shipments/shipment_detail.html', {'shipment': shipment})

def get_countries(request):
    countries = Country.objects.all().order_by('name')
    data = [{'id': country.id, 'name': country.name} for country in countries]
    return JsonResponse(data, safe=False)

def load_cities(request):
    country_id = request.GET.get('country_id')
    print(f"Loading cities for country_id: {country_id}")
    
    if not country_id:
        print("No country_id provided")
        return JsonResponse({'error': 'Country ID is required'}, status=400)
    
    try:
        cities = City.objects.filter(country_id=country_id).order_by('name')
        print(f"Found {cities.count()} cities")
        data = [{'id': city.id, 'name': city.name} for city in cities]
        return JsonResponse(data, safe=False)
    except Exception as e:
        print(f"Error loading cities: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)

def shipment_confirmation_pdf(request, shipment_id):
    """
    View for generating shipment confirmation PDF
    """
    shipment = get_object_or_404(Shipment, id=shipment_id)
    return generate_shipment_confirmation_pdf(shipment)

@staff_member_required
def shipment_detailed_pdf(request, shipment_id):
    """
    View for generating detailed shipment PDF (admin only)
    """
    shipment = get_object_or_404(Shipment, id=shipment_id)
    return generate_shipment_detailed_pdf(shipment)

@staff_member_required
def shipment_label_pdf(request, shipment_id):
    """
    View for generating shipment label PDF (admin only)
    """
    shipment = get_object_or_404(Shipment, id=shipment_id)
    return generate_shipment_label_pdf(shipment)

def shipment_pdf(request, awb_number):
    """Generate a PDF for the shipment details."""
    try:
        shipment = Shipment.objects.get(awb_number=awb_number)
        return generate_shipment_confirmation_pdf(shipment)
    except Shipment.DoesNotExist:
        return HttpResponse("Shipment not found", status=404)

def shipment_label_pdf(request, awb_number):
    """Generate a shipping label PDF."""
    try:
        shipment = Shipment.objects.get(awb_number=awb_number)
        pdf = generate_shipment_label_pdf(shipment)
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="label_{awb_number}.pdf"'
        return response
    except Shipment.DoesNotExist:
        return HttpResponse("Shipment not found", status=404)

