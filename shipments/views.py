from django.shortcuts import render, redirect, get_object_or_404
from .forms import ShipperForm, ShipmentForm
from .models import Shipment

def create_shipment(request):
    if request.method == "POST":
        shipper_form = ShipperForm(request.POST)
        shipment_form = ShipmentForm(request.POST)

        if shipper_form.is_valid() and shipment_form.is_valid():
            shipper = shipper_form.save()
            shipment = shipment_form.save(commit=False)
            shipment.shipper = shipper
            shipment.save()

            return redirect('shipment_detail', shipment_id=shipment.id)

    else:
        shipper_form = ShipperForm()
        shipment_form = ShipmentForm()

    return render(request, 'create_shipment.html', {
        'shipper_form': shipper_form,
        'shipment_form': shipment_form,
    })


def shipment_detail(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)
    return render(request, 'shipment_detail.html', {'shipment': shipment})