from django.db import transaction, models
from django.utils import timezone
from cities_light.models import Country, City
from django.core.exceptions import ValidationError
import random
import string

def generate_temp_number(prefix):
    """Generate a temporary unique number for pending shipments."""
    # Generate a random 8-digit number
    random_digits = ''.join(random.choices(string.digits, k=8))
    return f"{prefix}{random_digits}"

def generate_awb_number():
    """
    Generate a unique AWB number using atomic transaction to prevent race conditions.
    Returns a string in format 'AWB-XXXXXX' where XXXXXX is a sequential number.
    """
    with transaction.atomic():
        last_shipment = Shipment.objects.select_for_update().order_by('-id').first()
        if last_shipment and last_shipment.awb_number and last_shipment.awb_number.startswith('AWB-'):
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
        if last_shipment and last_shipment.reference_number and last_shipment.reference_number.startswith('REF-'):
            try:
                last_number = int(last_shipment.reference_number.replace('REF-', ''))
            except ValueError:
                last_number = 980102991
            new_number = last_number + 1
        else:
            new_number = 980102991 + 1
        return f"REF-{new_number:06d}"

def zip_code_validator(zip_code):
    if not zip_code.isdigit() :
        raise ValidationError("Invalid zip code")

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
    zip_code = models.CharField(max_length=10, blank=True, null=True, validators=[zip_code_validator])
    location = models.CharField(max_length=100, blank=True, null=True)
    contact_person = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    identity_image = models.ImageField(upload_to='shipper_identity/', null=True, blank=True, help_text="Upload a copy of your ID or passport")

    def __str__(self):
        return f"{self.shipper_name} - {self.city}"


def get_default_awb():
    """Generate a default AWB number for new shipments."""
    return generate_temp_number('PENDING')

def get_default_reference():
    """Generate a default reference number for new shipments."""
    return generate_temp_number('PENDING')

class Shipment(TimeStampedMixin):
    """Model for storing shipment information and tracking."""
    # Shipper Information
    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE, related_name="shipments")
    
    # Receiver Information
    receiver_name = models.CharField(max_length=100)
    receiver_address = models.TextField()
    receiver_country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name='receiver_shipments')
    receiver_city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='receiver_shipments')
    receiver_zip_code = models.CharField(max_length=10, blank=True, null=True, validators=[zip_code_validator])
    receiver_location = models.CharField(max_length=100, blank=True, null=True)
    receiver_contact_person = models.CharField(max_length=100)
    receiver_contact_number = models.CharField(max_length=20)
    receiver_mobile_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Shipment Details
    awb_number = models.CharField(max_length=50, unique=True, default=get_default_awb)
    reference_number = models.CharField(max_length=50, unique=True, default=get_default_reference)
    forwarder = models.CharField(max_length=50, blank=True, null=True)
    
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

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ]
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
    )
    
    # Package Details
    quantity = models.PositiveIntegerField()
    grossweight = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    chargeable_weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    length = models.DecimalField(max_digits=10, decimal_places=2)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    volumetricks = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    
    # Additional Information
    price_of_shipment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    item_description = models.TextField()
    special_instruction = models.TextField(blank=True, null=True)
    
    # Payment Information
    cod_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="COD in AED", default=0)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Base shipping cost", default=0)
    additional_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Additional fees")

    def clean(self):
        super().clean()
        # Calculate volumetric weight and chargeable weight
        if self.length and self.width and self.height and self.quantity:
            self.volumetricks = (self.length * self.width * self.height * self.quantity) / 5000
            self.chargeable_weight = max(self.volumetricks, self.grossweight)
        else:
            self.volumetricks = 0
            self.chargeable_weight = self.grossweight if self.grossweight else 0

    def save(self, *args, **kwargs):
        self.clean()  # Call clean to ensure calculations are done
        
        # Handle AWB and reference numbers based on payment status
        if self.payment_status == 'paid':
            try:
                # Generate permanent numbers for paid shipments
                if not self.awb_number or self.awb_number.startswith('PENDING'):
                    self.awb_number = generate_awb_number()
                if not self.reference_number or self.reference_number.startswith('PENDING'):
                    self.reference_number = generate_reference_number()
            except Exception as e:
                raise ValidationError(f"Error generating tracking numbers: {str(e)}")
        else:
            # Generate temporary numbers for pending shipments
            if not self.awb_number:
                self.awb_number = generate_temp_number('PENDING')
            if not self.reference_number:
                self.reference_number = generate_temp_number('PENDING')

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Shipment {self.awb_number}"



def validate_image_file(file):
    if not file.content_type.startswith('image'):
        raise ValidationError("File must be an image")
        
def validate_image_file_size(file):
    if file.size > 1024 * 1024 * 10:
        raise ValidationError("File must be less than 10MB")

class ShipmentImage(models.Model):
    """Model for storing shipment-related images."""
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='shipment_images/', validators=[validate_image_file, validate_image_file_size])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.shipment.awb_number}"