from django.contrib.auth.models import User

from django.db import models



# مدل کشور

class Country(models.Model):

    name = models.CharField(max_length=100, unique=True)



    def __str__(self):

        return self.name



# مدل شهر

class City(models.Model):

    name = models.CharField(max_length=100)

    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")



    def __str__(self):

        return f"{self.name}, {self.country.name}"



# مدل آدرس

class Address(models.Model):

    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)

    location = models.CharField(max_length=200, blank=True, null=True)  # محل دقیق (مثلاً خیابان و پلاک)

    full_address = models.TextField(blank=True, null=True)  # آدرس کامل به‌صورت متن آزاد



    def __str__(self):

        return f"{self.full_address} ({self.city}, {self.country})"



# مدل فرستنده (Shipper) - هر کاربر لاگین‌شده اطلاعات خودش رو داره

class Shipper(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # اتصال به یوزر لاگین شده

    name = models.CharField(max_length=100)

    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    contact_person = models.CharField(max_length=100)

    contact_number = models.CharField(max_length=20)

    mobile_number = models.CharField(max_length=20)



    def __str__(self):

        return self.name



# مدل محموله (Shipment)

class Shipment(models.Model):

    awb_number = models.CharField(max_length=20, unique=True)

    reference_number = models.CharField(max_length=50, blank=True, null=True)

    booking_date = models.DateField()

    booking_time = models.TimeField()



    shipper = models.ForeignKey(Shipper, on_delete=models.CASCADE)  # فرستنده

    receiver_name = models.CharField(max_length=100)

    receiver_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="receiver_shipments")

    receiver_contact_person = models.CharField(max_length=100)

    receiver_contact_number = models.CharField(max_length=20)

    receiver_mobile_number = models.CharField(max_length=20)



    product_type = models.CharField(max_length=100)

    pieces = models.PositiveIntegerField()

    weight = models.DecimalField(max_digits=10, decimal_places=2)

    v_weight = models.DecimalField(max_digits=10, decimal_places=2)

    c_weight = models.DecimalField(max_digits=10, decimal_places=2)

    cod_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    special_instruction = models.TextField(blank=True, null=True)

    item_description = models.TextField()



    def __str__(self):

        return f"Shipment {self.awb_number} - {self.receiver_name}"