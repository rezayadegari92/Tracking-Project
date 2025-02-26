from django.db import models


class Shipper(models.Model):
    shipper_name = models.CharField(max_length=100)
    address = models.TextField()
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    location = models.CharField(max_length=100, blank=True, null=True)
    contact_person = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    def __str__(self):
        return f"{self.shipper_name} - {self.city}"





class Shipment(models.Model):
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE, related_name="shipments")
    #receiver
    receiver_name = models.CharField(max_length=100)
    receiver_address = models.TextField()
    receiver_country = models.CharField(max_length=50)
    receiver_city = models.CharField(max_length=50)
    receiver_location = models.CharField(max_length=100, blank=True, null=True)
    receiver_contact_person = models.CharField(max_length=100)
    receiver_contact_number = models.CharField(max_length=20)
    receiver_mobile_number = models.CharField(max_length=20, blank=True, null=True)
    #shipment
    awb_number = models.CharField(max_length=50, unique=True)
    reference_number = models.CharField(max_length=50, blank=True, null=True)

    booking_date = models.DateField()
    booking_time = models.TimeField()
    product_type = models.CharField(max_length=50)
    pieces = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    v_weight = models.DecimalField(max_digits=10, decimal_places=2)
    c_weight = models.DecimalField(max_digits=10, decimal_places=2)
    item_description = models.TextField()
    special_instruction = models.TextField(blank=True, null=True)

    #payment
    cod_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="COD in AED")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Base shipping cost")
    additional_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Additional fees")
    def __str__(self):
        return f"Shipment {self.awb_number} "




