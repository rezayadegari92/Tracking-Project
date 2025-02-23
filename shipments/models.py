from django.db import models


class Sender(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    location = models.CharField(max_length=100, blank=True, null=True)
    contact_person = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    shipment = models.ForeignKey('Shipment', on_delete=models.CASCADE , related_name="receivers")
    def __str__(self):
        return f"{self.name} - {self.city}"



class Receiver(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    location = models.CharField(max_length=100, blank=True, null=True)
    contact_person = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.city}"


class Shipment(models.Model):
    awb_number = models.CharField(max_length=50, unique=True)
    reference_number = models.CharField(max_length=50, blank=True, null=True)
    sender = models.ForeignKey(Sender, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Receiver, on_delete=models.CASCADE)

    booking_date = models.DateField()
    booking_time = models.TimeField()
    product_type = models.CharField(max_length=50)
    pieces = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    v_weight = models.DecimalField(max_digits=10, decimal_places=2)
    c_weight = models.DecimalField(max_digits=10, decimal_places=2)
    item_description = models.TextField()
    special_instruction = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Shipment {self.awb_number} - {self.receiver.name}"


class ShipmentCost(models.Model):
    shipment = models.OneToOneField(Shipment, on_delete=models.CASCADE)
    cod_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="COD in AED")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Base shipping cost")
    additional_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Additional fees")

    def total_cost(self):
        return self.base_price + self.additional_charges + self.cod_amount

    def __str__(self):
        return f"Cost for {self.shipment.awb_number}"

