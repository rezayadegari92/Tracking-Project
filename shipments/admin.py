from django.contrib import admin

from .models import Country, City, Address, Shipper, Shipment



@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):

    list_display = ("name",)

    search_fields = ("name",)



@admin.register(City)
class CityAdmin(admin.ModelAdmin):

    list_display = ("name", "country")

    list_filter = ("country",)

    search_fields = ("name", "country__name")







@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):

    list_display = ("full_address", "city", "country")

    list_filter = ("city", "country")

    search_fields = ("full_address", "city__name", "country__name")

    ordering = ("city",)







@admin.register(Shipper)
class ShipperAdmin(admin.ModelAdmin):

    list_display = ("name", "contact_person", "contact_number", "mobile_number", "get_address")

    search_fields = ("name", "contact_person", "contact_number", "mobile_number")

    list_filter = ("address__city", "address__country")



    def get_address(self, obj):

        return obj.address.full_address if obj.address else "No Address"

    get_address.short_description = "Address"







@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):

    list_display = (

        "awb_number", "booking_date", "booking_time",

        "shipper", "receiver_name", "get_receiver_address",

        "pieces", "weight", "cod_amount"

    )

    list_filter = ("booking_date", "shipper", "receiver_address__city", "receiver_address__country")

    search_fields = ("awb_number", "reference_number", "receiver_name", "shipper__name")

    date_hierarchy = "booking_date"

    ordering = ("-booking_date",)

    list_per_page = 20



    def get_receiver_address(self, obj):

        return obj.receiver_address.full_address if obj.receiver_address else "No Address"

    get_receiver_address.short_description = "Receiver Address"







from django.contrib import admin



admin.site.site_header = "Shipment Management Admin"

admin.site.site_title = "Shipment Admin"

admin.site.index_title = "Welcome to Shipment Dashboard"



