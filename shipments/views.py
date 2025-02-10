
from django.shortcuts import render, redirect

from .forms import ShipmentForm



def create_shipment(request):

    if request.method == "POST":

        form = ShipmentForm(request.POST, user=request.user)

        if form.is_valid():

            form.save()

            return redirect('shipment_form')  # بعد از ذخیره، کاربر رو به لیست محموله‌ها هدایت کن

    else:

        form = ShipmentForm(user=request.user)



    return render(request, 'shipment_form.html', {'form': form})

