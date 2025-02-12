from django.contrib import admin

from .models import Shipment



@admin.register(Shipment)

class ShipmentAdmin(admin.ModelAdmin):

    list_display = ('awb_number', 'shipper', 'receiver', 'booking_date', 'product_type', 'pieces', 'cod_amount')

    search_fields = ('awb_number', 'shipper', 'receiver')

    list_filter = ('booking_date', 'shipper_country', 'receiver_country')