from django.db import models
from django.utils import timezone
from cities_light.models import Country, City


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Shipper(TimeStampedMixin):
    shipper_name = models.CharField(max_length=100)
    address = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    contact_person = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    def __str__(self):
        return f"{self.shipper_name} - {self.city}"





class Shipment(TimeStampedMixin):
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE, related_name="shipments")
    #receiver
    receiver_name = models.CharField(max_length=100)
    receiver_address = models.TextField()
    receiver_country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    receiver_city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    receiver_location = models.CharField(max_length=100, blank=True, null=True)
    receiver_contact_person = models.CharField(max_length=100)
    receiver_contact_number = models.CharField(max_length=20)
    receiver_mobile_number = models.CharField(max_length=20, blank=True, null=True)
    #shipment
    #thise are generated in save method from awb_number_generator function
    awb_number = models.CharField(max_length=50, unique=True)
    reference_number = models.CharField(max_length=50, blank=True, null=True)
    forwarder = models.CharField(max_length=50,default="Dubai")
    PRODUCT_TYPE_CHOICES = [
        ('doc', 'Doc'),
        ('no_doc', 'No Doc'),
    ]
    product_type = models.CharField(
        max_length=10,
        choices=PRODUCT_TYPE_CHOICES,
        default='doc',
    )
    SERVICE_TYPE_CHOICES = [
        ('inbound', 'In Bound'),
        ('outbound', 'Out Bound'),
        ('pick-up-visa', 'Pick-Up_Visa'),
    ]
    service= models.CharField(
        max_length=20,
        choices=SERVICE_TYPE_CHOICES,
        default='doc',
    )
    quantity = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    v_weight = models.DecimalField(max_digits=10, decimal_places=2)
    c_weight = models.DecimalField(max_digits=10, decimal_places=2)
    #volumetrick is result of length * width * height / 5000 
    volumetricks = models.DecimalField(max_digits=10, decimal_places=3)
    price_of_shipment = models.DecimalField(max_digits=10, decimal_places=2)
    item_description = models.TextField()
    special_instruction = models.TextField(blank=True, null=True)

    #payment
    cod_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="COD in AED")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Base shipping cost")
    additional_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Additional fees")

    #this function is used to generate awb number  from some number and it bigger than 1000000 and get bigger one by 1
    def awb_number_generator(self):
        last_awb_number = Shipment.objects.order_by('-awb_number').first()
        if last_awb_number:
            last_number = int(last_awb_number.awb_number.split('-')[-1])
            new_number = last_number + 1
            return f"AWB-{new_number:06d}"
        else:
            return f"AWB-000001"
    def reference_number_generator(self):
        last_reference_number = Shipment.objects.order_by('-reference_number').first()
        if last_reference_number:
            last_number = int(last_reference_number.reference_number.split('-')[-1])
            new_number = last_number + 1
            return f"REF-{new_number:06d}"
        else:
            return f"REF-000001"
    def save(self, *args, **kwargs):
        self.volumetricks = self.length * self.width * self.height / 5000
        self.awb_number = self.awb_number_generator()
        self.reference_number = self.reference_number_generator()



    def __str__(self):
        return f"Shipment {self.awb_number} "




class ShipmentImage(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.shipment.name}"