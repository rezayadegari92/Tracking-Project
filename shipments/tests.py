from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import Shipper, Shipment, ShipmentImage
from cities_light.models import Country, City


class ShipmentModelTest(TestCase):
    def setUp(self):
        # Create test country and city
        self.country = Country.objects.create(name='Test Country')
        self.city = City.objects.create(name='Test City', country=self.country)
        
        # Create test shipper
        self.shipper = Shipper.objects.create(
            shipper_name='Test Shipper',
            address='Test Address',
            country=self.country,
            city=self.city,
            contact_person='Test Person',
            contact_number='1234567890'
        )

    def test_create_shipment(self):
        """Test creating a basic shipment"""
        shipment = Shipment.objects.create(
            shipper=self.shipper,
            receiver_name='Test Receiver',
            receiver_address='Test Address',
            receiver_country=self.country,
            receiver_city=self.city,
            receiver_contact_person='Test Person',
            receiver_contact_number='1234567890',
            quantity=1,
            grossweight=Decimal('1.00'),
            width=Decimal('10.00'),
            length=Decimal('10.00'),
            height=Decimal('10.00'),
            price_of_shipment=Decimal('100.00'),
            item_description='Test Item',
            cod_amount=Decimal('0.00'),
            base_price=Decimal('100.00')
        )
        
        self.assertIsNotNone(shipment.awb_number)
        self.assertIsNotNone(shipment.reference_number)
        self.assertEqual(shipment.volumetricks, Decimal('0.200'))  # (10*10*10)/5000

    def test_awb_number_generation(self):
        """Test AWB number generation sequence"""
        shipment1 = Shipment.objects.create(
            shipper=self.shipper,
            receiver_name='Test Receiver 1',
            receiver_address='Test Address',
            receiver_country=self.country,
            receiver_city=self.city,
            receiver_contact_person='Test Person',
            receiver_contact_number='1234567890',
            quantity=1,
            grossweight=Decimal('1.00'),
            width=Decimal('10.00'),
            length=Decimal('10.00'),
            height=Decimal('10.00'),
            price_of_shipment=Decimal('100.00'),
            item_description='Test Item',
            cod_amount=Decimal('0.00'),
            base_price=Decimal('100.00')
        )
        
        shipment2 = Shipment.objects.create(
            shipper=self.shipper,
            receiver_name='Test Receiver 2',
            receiver_address='Test Address',
            receiver_country=self.country,
            receiver_city=self.city,
            receiver_contact_person='Test Person',
            receiver_contact_number='1234567890',
            quantity=1,
            grossweight=Decimal('1.00'),
            width=Decimal('10.00'),
            length=Decimal('10.00'),
            height=Decimal('10.00'),
            price_of_shipment=Decimal('100.00'),
            item_description='Test Item',
            cod_amount=Decimal('0.00'),
            base_price=Decimal('100.00')
        )
        
        self.assertNotEqual(shipment1.awb_number, shipment2.awb_number)
        self.assertTrue(shipment1.awb_number.startswith('AWB-'))
        self.assertTrue(shipment2.awb_number.startswith('AWB-'))

    def test_reference_number_generation(self):
        """Test reference number generation sequence"""
        shipment1 = Shipment.objects.create(
            shipper=self.shipper,
            receiver_name='Test Receiver 1',
            receiver_address='Test Address',
            receiver_country=self.country,
            receiver_city=self.city,
            receiver_contact_person='Test Person',
            receiver_contact_number='1234567890',
            quantity=1,
            grossweight=Decimal('1.00'),
            width=Decimal('10.00'),
            length=Decimal('10.00'),
            height=Decimal('10.00'),
            price_of_shipment=Decimal('100.00'),
            item_description='Test Item',
            cod_amount=Decimal('0.00'),
            base_price=Decimal('100.00')
        )
        
        shipment2 = Shipment.objects.create(
            shipper=self.shipper,
            receiver_name='Test Receiver 2',
            receiver_address='Test Address',
            receiver_country=self.country,
            receiver_city=self.city,
            receiver_contact_person='Test Person',
            receiver_contact_number='1234567890',
            quantity=1,
            grossweight=Decimal('1.00'),
            width=Decimal('10.00'),
            length=Decimal('10.00'),
            height=Decimal('10.00'),
            price_of_shipment=Decimal('100.00'),
            item_description='Test Item',
            cod_amount=Decimal('0.00'),
            base_price=Decimal('100.00')
        )
        
        self.assertNotEqual(shipment1.reference_number, shipment2.reference_number)
        self.assertTrue(shipment1.reference_number.startswith('REF-'))
        self.assertTrue(shipment2.reference_number.startswith('REF-'))

    def test_shipment_image_creation(self):
        """Test creating a shipment with an image"""
        shipment = Shipment.objects.create(
            shipper=self.shipper,
            receiver_name='Test Receiver',
            receiver_address='Test Address',
            receiver_country=self.country,
            receiver_city=self.city,
            receiver_contact_person='Test Person',
            receiver_contact_number='1234567890',
            quantity=1,
            grossweight=Decimal('1.00'),
            width=Decimal('10.00'),
            length=Decimal('10.00'),
            height=Decimal('10.00'),
            price_of_shipment=Decimal('100.00'),
            item_description='Test Item',
            cod_amount=Decimal('0.00'),
            base_price=Decimal('100.00')
        )
        
        image = ShipmentImage.objects.create(
            shipment=shipment,
            image='test_image.jpg'
        )
        
        self.assertEqual(image.shipment, shipment)
        self.assertEqual(str(image), f"Image for {shipment.awb_number}")
