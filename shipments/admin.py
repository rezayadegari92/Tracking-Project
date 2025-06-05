from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Shipper, Shipment, ShipmentImage


@admin.register(Shipper)
class ShipperAdmin(admin.ModelAdmin):
    list_display = ('shipper_name', 'city', 'country', 'contact_person', 'contact_number')
    search_fields = ('shipper_name', 'contact_person', 'contact_number')
    list_filter = ('country', 'city')
    fieldsets = (
        ('Basic Information', {
            'fields': ('shipper_name', 'address')
        }),
        ('Location', {
            'fields': ('country', 'city', 'location')
        }),
        ('Contact Information', {
            'fields': ('contact_person', 'contact_number', 'mobile_number')
        }),
    )


class ShipmentImageInline(admin.TabularInline):
    model = ShipmentImage
    extra = 1


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('awb_number', 'shipper', 'receiver_name', 'receiver_city', 'pdf_buttons')
    list_filter = ('product_type', 'service', 'receiver_country', 'receiver_city')
    search_fields = ('awb_number', 'reference_number', 'receiver_name', 'receiver_contact_person')
    readonly_fields = ('awb_number', 'reference_number', 'created_at', 'updated_at')
    inlines = [ShipmentImageInline]
    
    def pdf_buttons(self, obj):
        detailed_url = reverse('shipment_detailed_pdf', args=[obj.id])
        label_url = reverse('shipment_label_pdf', args=[obj.id])
        return format_html(
            '<a class="button" href="{}">Detailed PDF</a>&nbsp;'
            '<a class="button" href="{}">Label PDF</a>',
            detailed_url, label_url
        )
    pdf_buttons.short_description = 'PDF Downloads'

    fieldsets = (
        ('Tracking Information', {
            'fields': ('awb_number', 'reference_number', 'forwarder')
        }),
        ('Shipper Information', {
            'fields': ('shipper',)
        }),
        ('Receiver Information', {
            'fields': (
                'receiver_name', 'receiver_address', 'receiver_country',
                'receiver_city', 'receiver_location', 'receiver_contact_person',
                'receiver_contact_number', 'receiver_mobile_number'
            )
        }),
        ('Shipment Details', {
            'fields': (
                'product_type', 'service', 'quantity', 'grossweight',
                'width', 'length', 'height', 'volumetricks'
            )
        }),
        ('Additional Information', {
            'fields': ('item_description', 'special_instruction')
        }),
        ('Payment Information', {
            'fields': ('price_of_shipment', 'cod_amount', 'base_price', 'additional_charges')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ShipmentImage)
class ShipmentImageAdmin(admin.ModelAdmin):
    list_display = ('shipment', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('shipment__awb_number',)