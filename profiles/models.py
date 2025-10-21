from django.db import models
from cities_light.models import Country, City
from shipments.models import zip_code_validator
from django.conf import settings
import uuid

class Address(models.Model):
    address_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    address = models.TextField(max_length=500)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True, validators=[zip_code_validator])
    location = models.CharField(max_length=100, blank=True, null=True)
    contact_number = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    identity_image = models.ImageField(upload_to='shipper_identity/', null=True, blank=True, help_text="Upload a copy of your ID or passport")
    default_address = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # ensure only one default address per user
        if self.default_address:
            Address.objects.filter(user=self.user).exclude(pk=self.pk).update(default_address=False)

    def __str__(self):
        return f"{self.user} - {self.city}"
