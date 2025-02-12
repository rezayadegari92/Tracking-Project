from django.shortcuts import render, redirect

from .models import Shipment

from .forms import ShipmentForm



def create_shipment(request):

    if request.method == "POST":

        form = ShipmentForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('shipment_list')  # Redirect to shipment list page

    else:

        form = ShipmentForm()

    return render(request, 'shipment_form.html', {'form': form})



def shipment_list(request):

    shipments = Shipment.objects.all()

    return render(request, 'shipment_list.html', {'shipments': shipments})

