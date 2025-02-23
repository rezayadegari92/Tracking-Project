from django.contrib import admin
from .models import Sender, Receiver, Shipment, ShipmentCost

# چون الان Sender و Receiver به Shipment متصل هستند، این کد بدون خطا کار خواهد کرد
class SenderInline(admin.StackedInline):
    model = Sender
    extra = 1
    can_delete = False

class ReceiverInline(admin.StackedInline):
    model = Receiver
    extra = 1
    can_delete = False

class ShipmentCostInline(admin.StackedInline):
    model = ShipmentCost
    extra = 1
    can_delete = False

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('awb_number', 'sender', 'receiver', 'booking_date', 'product_type', 'pieces')
    search_fields = ('awb_number', 'sender__name', 'receiver__name')
    list_filter = ('booking_date', 'product_type')
    inlines = [ShipmentCostInline]

@admin.register(Sender)
class SenderAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'contact_number')
    search_fields = ('name', 'city')

@admin.register(Receiver)
class ReceiverAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'contact_number')
    search_fields = ('name', 'city')

@admin.register(ShipmentCost)
class ShipmentCostAdmin(admin.ModelAdmin):
    list_display = ('shipment', 'cod_amount', 'base_price', 'additional_charges', 'total_cost')
    readonly_fields = ('total_cost',)

    def total_cost(self, obj):
        return obj.total_cost()
    total_cost.short_description = "Total Cost (AED)"