from django.shortcuts import render, redirect
from .forms import ShipmentForm, SenderForm, ReceiverForm, ShipmentCostForm

def create_shipment(request):
    if request.method == "POST":
        shipment_form = ShipmentForm(request.POST)
        sender_form = SenderForm(request.POST)
        receiver_form = ReceiverForm(request.POST)
        shipment_cost_form = ShipmentCostForm(request.POST)

        if shipment_form.is_valid() and sender_form.is_valid() and receiver_form.is_valid() and shipment_cost_form.is_valid():
            sender = sender_form.save()
            receiver = receiver_form.save()
            shipment = shipment_form.save(commit=False)
            shipment.sender = sender
            shipment.receiver = receiver
            shipment.save()

            shipment_cost = shipment_cost_form.save(commit=False)
            shipment_cost.shipment = shipment
            shipment_cost.save()

            return redirect('shipment_list')  # بعد از ذخیره، کاربر رو به لیست سفارشات هدایت کن

    else:
        shipment_form = ShipmentForm()
        sender_form = SenderForm()
        receiver_form = ReceiverForm()
        shipment_cost_form = ShipmentCostForm()

    return render(request, 'create_shipment.html', {
        'shipment_form': shipment_form,
        'sender_form': sender_form,
        'receiver_form': receiver_form,
        'shipment_cost_form': shipment_cost_form,
    })
from .models import Shipment
def shipment_list(request, shipment_id):
    shipment = Shipment.objects.get(id=shipment_id)
    return  render(request, 'shipment_list', {'shipment':shipment})