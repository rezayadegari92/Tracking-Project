from django.contrib import admin
from .models import Sender, Receiver, Shipment, ShipmentCost

# مدل فرستنده به صورت جداگانه
class SenderAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'contact_number')
    search_fields = ('name', 'city')

# مدل گیرنده به صورت جداگانه
class ReceiverInline(admin.StackedInline):
    model = Receiver
    extra = 1

# مدل هزینه به صورت جداگانه
class ShipmentCostInline(admin.StackedInline):
    model = ShipmentCost
    extra = 1

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('awb_number', 'sender', 'receiver', 'booking_date', 'product_type', 'pieces')
    search_fields = ('awb_number', 'sender__name', 'receiver__name')
    list_filter = ('booking_date', 'product_type')

    # نمایش فرستنده، گیرنده و هزینه در یکجا
    inlines = [ReceiverInline, ShipmentCostInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # نمایش تمام فیلدها
        return form

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