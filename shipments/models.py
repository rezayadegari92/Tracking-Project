from django.db import models

class Shipment(models.Model):
    # Sender Details

    awb_number = models.CharField(max_length=50, unique=True)

    reference_number = models.CharField(max_length=50, blank=True, null=True)

    shipper = models.CharField(max_length=100)

    shipper_address = models.TextField()

    shipper_country = models.CharField(max_length=50)

    shipper_city = models.CharField(max_length=50)

    shipper_location = models.CharField(max_length=100, blank=True, null=True)

    shipper_contact_person = models.CharField(max_length=100)

    shipper_contact_number = models.CharField(max_length=20)

    shipper_mobile_number = models.CharField(max_length=20, blank=True, null=True)

    product_type = models.CharField(max_length=50)

    pieces = models.PositiveIntegerField()

    special_instruction = models.TextField(blank=True, null=True)

    # Receiver Details

    booking_date = models.DateField()

    booking_time = models.TimeField()

    receiver = models.CharField(max_length=100)

    receiver_address = models.TextField()

    receiver_country = models.CharField(max_length=50)

    receiver_city = models.CharField(max_length=50)

    receiver_location = models.CharField(max_length=100, blank=True, null=True)

    receiver_contact_person = models.CharField(max_length=100)

    receiver_contact_number = models.CharField(max_length=20)

    receiver_mobile_number = models.CharField(max_length=20, blank=True, null=True)

    # Shipment Details

    weight = models.DecimalField(max_digits=10, decimal_places=2)

    v_weight = models.DecimalField(max_digits=10, decimal_places=2)

    c_weight = models.DecimalField(max_digits=10, decimal_places=2)

    cod_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="COD in AED")

    item_description = models.TextField()

    def __str__(self):
        return f"Shipment {self.awb_number} - {self.receiver}"


