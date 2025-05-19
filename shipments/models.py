from django.db import transaction, models
from django.utils import timezone
from cities_light.models import Country, City


def generate_awb_number():
    """
    Generate a unique AWB number using atomic transaction to prevent race conditions.
    Returns a string in format 'AWB-XXXXXX' where XXXXXX is a sequential number.
    """
    with transaction.atomic():
        last_shipment = Shipment.objects.select_for_update().order_by('-id').first()
        if last_shipment and last_shipment.awb_number:
            try:
                last_number = int(last_shipment.awb_number.replace('AWB-', ''))
            except ValueError:
                last_number = 980102991
            new_number = last_number + 1
        else:
            new_number = 980102991 + 1
        return f"AWB-{new_number:06d}"


def generate_reference_number():
    """
    Generate a unique reference number using atomic transaction to prevent race conditions.
    Returns a string in format 'REF-XXXXXX' where XXXXXX is a sequential number.
    """
    with transaction.atomic():
        last_shipment = Shipment.objects.select_for_update().order_by('-id').first()
        if last_shipment and last_shipment.reference_number:
            try:
                last_number = int(last_shipment.reference_number.replace('REF-', ''))
            except ValueError:
                last_number = 980102991
            new_number = last_number + 1
        else:
            new_number = 980102991 + 1
        return f"REF-{new_number:06d}"


class TimeStampedMixin(models.Model):
    """Abstract base model that provides created_at and updated_at timestamps."""
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Shipper(TimeStampedMixin):
    """Model for storing shipper information."""
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
    """Model for storing shipment information and tracking."""
    # Shipper Information
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE, related_name="shipments")
    
    # Receiver Information
    receiver_name = models.CharField(max_length=100)
    receiver_address = models.TextField()
    receiver_country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name='receiver_shipments')
    receiver_city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='receiver_shipments')
    receiver_location = models.CharField(max_length=100, blank=True, null=True)
    receiver_contact_person = models.CharField(max_length=100)
    receiver_contact_number = models.CharField(max_length=20)
    receiver_mobile_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Shipment Details
    awb_number = models.CharField(max_length=50, unique=True)
    reference_number = models.CharField(max_length=50, blank=True, null=True, unique=True)
    forwarder = models.CharField(max_length=50, default="Dubai")
    
    PRODUCT_TYPE_CHOICES = [
        ('doc', 'Document'),
        ('no_doc', 'Non-Document'),
    ]
    product_type = models.CharField(
        max_length=10,
        choices=PRODUCT_TYPE_CHOICES,
        default='doc',
    )
    
    SERVICE_TYPE_CHOICES = [
        ('inbound', 'In Bound'),
        ('outbound', 'Out Bound'),
        ('pick-up-visa', 'Pick-Up Visa'),
    ]
    service = models.CharField(
        max_length=20,
        choices=SERVICE_TYPE_CHOICES,
        default='outbound',
    )
    
    # Package Details
    quantity = models.PositiveIntegerField()
    grossweight = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    length = models.DecimalField(max_digits=10, decimal_places=2)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    volumetricks = models.DecimalField(max_digits=10, decimal_places=3)
    
    # Additional Information
    price_of_shipment = models.DecimalField(max_digits=10, decimal_places=2)
    item_description = models.TextField()
    special_instruction = models.TextField(blank=True, null=True)
    
    # Payment Information
    cod_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="COD in AED")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Base shipping cost")
    additional_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Additional fees")

    def save(self, *args, **kwargs):
        """Override save method to generate AWB and reference numbers and calculate volumetric weight."""
        if not self.awb_number:
            self.awb_number = generate_awb_number()
        if not self.reference_number:
            self.reference_number = generate_reference_number()
        self.volumetricks = self.length * self.width * self.height / 5000
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Shipment {self.awb_number}"


class ShipmentImage(models.Model):
    """Model for storing shipment-related images."""
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='shipment_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.shipment.awb_number}"