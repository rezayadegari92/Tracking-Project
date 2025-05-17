# from django.contrib import admin
# from .models import Shipper, Shipment

# @admin.register(Shipper)
# class ShipperAdmin(admin.ModelAdmin):
#     list_display = ('shipper_name', 'city', 'contact_number')

# @admin.register(Shipment)
# class ShipmentAdmin(admin.ModelAdmin):
#     list_display = ('awb_number', 'shipper', 'receiver_name', 'booking_date', 'product_type', 'pieces', 'cod_amount')
#     list_filter = ('booking_date', 'product_type', 'shipper__city')
#     search_fields = ('awb_number', 'receiver_name', 'shipper__shipper_name')